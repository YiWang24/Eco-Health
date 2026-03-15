"""Railtracks agentic workflow orchestrator for meal planning."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from typing import Any

import railtracks as rt

from app.agents.io_contracts import AgentPlanInputV1, AgentPlanOutputV1
from app.agents.reflection import apply_reflection
from app.agents.rt_config import get_llm, get_vector_store
from app.agents.schemas import AgentDraftBundle, RtRecommendationOutput
from app.agents.tools import (
    calculate_meal_macros,
    decompose_cooking_workflow,
    generate_grocery_gap_tool,
    retrieve_recipe_candidates,
    schedule_proactive_prep,
)
from app.core.config import Settings, get_settings
from app.schemas.contracts import (
    DecisionBlock,
    ExecutionPlanBlock,
    GroceryItem,
    GroceryPlanBlock,
    MealPlanBlock,
    MemoryUpdatesBlock,
    PlanRequest,
    ReflectionBlock,
)
from app.services.execution_planning import build_cooking_dag_tasks, build_proactive_prep_windows
from app.services.planner import retrieve_recipe_candidates as retrieve_recipe_candidates_service
from app.agents.rag_pipeline import get_rag_pipeline


class RailtracksAgenticWorkflow:
    """Stage-based Railtracks workflow following the agentic design loop."""

    def __init__(self, settings: Settings):
        self.settings = settings
        resolved_api_key = (settings.gemini_api_key or "").strip()
        self._enabled = bool(
            settings.railtracks_enabled
            and resolved_api_key
            and (settings.gemini_model or settings.railtracks_model)
        )
        self._llm = None
        self._vector_store = None
        self._agent = None
        self._rag = get_rag_pipeline()

        if not self._enabled:
            return

        try:
            self._llm = get_llm()
            self._vector_store = get_vector_store()
            self._agent = self._build_agent()
        except Exception:  # pragma: no cover - environment dependent
            self._enabled = False

    def _build_agent(self):
        instruction = (
            "You are Eco-Health Agentic Dietitian planner. "
            "Given user constraints, prioritized ingredients, retrieved context, and a candidate recipe, "
            "produce strict JSON fields: recipe_title, steps, substitutions, spoilage_alerts, grocery_gap, "
            "nutrition_summary, rationale, confidence."
        )
        tools = [
            retrieve_recipe_candidates,
            calculate_meal_macros,
            generate_grocery_gap_tool,
            decompose_cooking_workflow,
            schedule_proactive_prep,
        ]
        if hasattr(rt, "Agent"):
            if self._vector_store:
                return rt.Agent(
                    name="eco_health_agentic_planner",
                    llm=self._llm,
                    instruction=instruction,
                    tools=tools,
                    vector_store=self._vector_store,
                    output_schema=RtRecommendationOutput,
                )
            return rt.Agent(
                name="eco_health_agentic_planner",
                llm=self._llm,
                instruction=instruction,
                tools=tools,
                output_schema=RtRecommendationOutput,
            )

        rag_config = rt.RagConfig(vector_store=self._vector_store, top_k=3) if self._vector_store else None
        return rt.agent_node(
            name="eco_health_agentic_planner",
            llm=self._llm,
            system_message=instruction,
            tool_nodes=tools,
            rag=rag_config,
            output_schema=RtRecommendationOutput,
        )

    async def recommend_async(self, agent_input: AgentPlanInputV1) -> AgentPlanOutputV1:
        if not self._enabled or not self._agent:
            raise RuntimeError("Railtracks workflow is disabled or unavailable")

        trace_notes: list[str] = ["workflow:railtracks-agentic"]

        request = self.perceive(agent_input)
        trace_notes.append("stage:PERCEIVE")

        priority_signals = self.prioritize(request)
        trace_notes.append("stage:PRIORITIZE")

        retrieved_context = self.retrieve_context(request, priority_signals)
        trace_notes.append("stage:RETRIEVE")

        candidates = self.query_recipe(request, priority_signals, retrieved_context)
        trace_notes.append(f"stage:QUERY_RECIPE:candidates={len(candidates)}")

        output = await self.reflect_and_retry(
            request=request,
            candidates=candidates,
            priority_signals=priority_signals,
            retrieved_context=retrieved_context,
            trace_notes=trace_notes,
        )
        trace_notes.append("stage:REFLECT")

        final_execution = self.finalize_execution(output.meal_plan.steps)
        output.execution_plan = final_execution
        output.trace_notes = trace_notes
        trace_notes.append("stage:FINALIZE")
        return output

    @staticmethod
    def perceive(agent_input: AgentPlanInputV1) -> PlanRequest:
        """Perceive stage: normalize incoming runtime context."""

        return agent_input.to_plan_request()

    @staticmethod
    def prioritize(request: PlanRequest) -> dict[str, Any]:
        """Prioritize stage: identify spoilage and hard constraints."""

        expiring = []
        if request.inventory and request.inventory.items:
            expiring = sorted(
                [
                    item.ingredient
                    for item in request.inventory.items
                    if item.expires_in_days is not None and item.expires_in_days <= 2
                ]
            )
        return {
            "expiring_ingredients": expiring[:5],
            "allergies": request.constraints.allergies,
            "dietary_restrictions": request.constraints.dietary_restrictions,
            "max_cook_time_minutes": request.constraints.max_cook_time_minutes,
        }

    def retrieve_context(self, request: PlanRequest, priority_signals: dict[str, Any]) -> list[dict[str, Any]]:
        """Retrieve stage: gather vector/keyword recipe context."""

        _ = priority_signals
        try:
            return self._rag.retrieve_context(request.inventory, request.constraints, limit=5)
        except Exception:
            return []

    @staticmethod
    def query_recipe(
        request: PlanRequest,
        priority_signals: dict[str, Any],
        retrieved_context: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Query recipe stage: produce candidate recipe set."""

        _ = priority_signals
        candidates = retrieve_recipe_candidates_service(
            request.inventory,
            constraints=request.constraints,
            limit=5,
        )
        if candidates:
            return candidates

        rag_backfill = [item.get("full_recipe") for item in retrieved_context if isinstance(item.get("full_recipe"), dict)]
        return [item for item in rag_backfill if item]

    async def formulate_plan(
        self,
        *,
        request: PlanRequest,
        candidate_recipe: dict[str, Any] | None,
        priority_signals: dict[str, Any],
        retrieved_context: list[dict[str, Any]],
        attempt: int,
    ) -> tuple[AgentDraftBundle, dict[str, Any]]:
        """Formulate stage: use Railtracks to draft recommendation payload."""

        prompt = self._build_prompt(
            request=request,
            candidate_recipe=candidate_recipe,
            priority_signals=priority_signals,
            retrieved_context=retrieved_context,
            attempt=attempt,
        )
        if hasattr(self._agent, "run_async"):
            result = await self._agent.run_async(prompt)
        else:
            result = await rt.call(self._agent, prompt)

        content = getattr(result, "content", result)
        if not content:
            raise ValueError("No Railtracks response content produced")

        parsed = self._parse_railtracks_output(content)
        bundle = AgentDraftBundle(
            recipe_title=parsed.recipe_title,
            steps=parsed.steps,
            substitutions=parsed.substitutions,
            spoilage_alerts=parsed.spoilage_alerts,
            grocery_gap=[GroceryItem.model_validate(item.model_dump()) for item in parsed.grocery_gap],
            nutrition_summary=parsed.nutrition_summary.model_dump(),
        )
        decision = {
            "rationale": parsed.rationale or parsed.confidence_note,
            "confidence": parsed.confidence,
        }
        return bundle, decision

    async def reflect_and_retry(
        self,
        *,
        request: PlanRequest,
        candidates: list[dict[str, Any]],
        priority_signals: dict[str, Any],
        retrieved_context: list[dict[str, Any]],
        trace_notes: list[str],
    ) -> AgentPlanOutputV1:
        """Reflect stage with bounded retries."""

        max_attempts = 3
        adjustments: list[str] = []
        final_bundle: AgentDraftBundle | None = None
        final_violations: list[dict[str, Any]] = []
        final_decision_meta: dict[str, Any] = {}
        status = "ok"
        attempts_used = 0

        for attempt in range(1, max_attempts + 1):
            attempts_used = attempt
            candidate_recipe = candidates[(attempt - 1) % len(candidates)] if candidates else None
            bundle, decision_meta = await self.formulate_plan(
                request=request,
                candidate_recipe=candidate_recipe,
                priority_signals=priority_signals,
                retrieved_context=retrieved_context,
                attempt=attempt,
            )

            reflected_bundle, notes, violations = apply_reflection(bundle, request)
            trace_notes.append(f"attempt:{attempt}")
            trace_notes.extend([f"reflection:{note}" for note in notes])
            trace_notes.extend([f"violation:{item.get('type', 'unknown')}" for item in violations])

            adjustments.extend(notes)
            final_bundle = reflected_bundle
            final_violations = violations
            final_decision_meta = decision_meta

            if not violations:
                status = "ok"
                break
            status = "adjusted_with_violations"

        if final_bundle is None:
            raise RuntimeError("Unable to formulate recommendation after retries")

        return AgentPlanOutputV1(
            decision=DecisionBlock(
                recipe_title=final_bundle.recipe_title,
                rationale=final_decision_meta.get("rationale"),
                confidence=final_decision_meta.get("confidence"),
            ),
            meal_plan=MealPlanBlock(
                steps=final_bundle.steps,
                nutrition_summary=final_bundle.nutrition_summary,
                substitutions=final_bundle.substitutions,
                spoilage_alerts=final_bundle.spoilage_alerts,
            ),
            grocery_plan=GroceryPlanBlock(
                missing_ingredients=final_bundle.grocery_gap,
                optimized_grocery_list=final_bundle.grocery_gap,
                estimated_gap_cost=float(len(final_bundle.grocery_gap) * 2.0),
            ),
            execution_plan=ExecutionPlanBlock(),
            reflection=ReflectionBlock(
                status=status,
                attempts=attempts_used,
                violations=final_violations,
                adjustments=adjustments,
            ),
            memory_updates=MemoryUpdatesBlock(
                short_term_updates=["inventory_used", "constraints_applied", "chat_context_applied"],
                long_term_metric_deltas={},
            ),
            trace_notes=trace_notes,
            mode="railtracks-agentic",
        )

    @staticmethod
    def finalize_execution(steps: list[str]) -> ExecutionPlanBlock:
        """Finalize stage: build non-persisted execution plan preview."""

        tasks = build_cooking_dag_tasks(steps)
        windows = build_proactive_prep_windows(tasks)
        return ExecutionPlanBlock(
            calendar_blocks=[],
            cooking_dag_tasks=tasks,
            proactive_prep_windows=windows,
        )

    @staticmethod
    def _parse_railtracks_output(content: Any) -> RtRecommendationOutput:
        if isinstance(content, RtRecommendationOutput):
            return content

        if isinstance(content, dict):
            return RtRecommendationOutput.model_validate(content)

        if hasattr(content, "model_dump"):
            return RtRecommendationOutput.model_validate(content.model_dump())

        content = str(content).strip()
        try:
            return RtRecommendationOutput.model_validate_json(content)
        except Exception:
            pass

        match = re.search(r"\{.*\}", content, re.DOTALL)
        if not match:
            raise ValueError("Unable to parse Railtracks JSON output")
        payload = json.loads(match.group(0))
        return RtRecommendationOutput.model_validate(payload)

    @staticmethod
    def _build_prompt(
        *,
        request: PlanRequest,
        candidate_recipe: dict[str, Any] | None,
        priority_signals: dict[str, Any],
        retrieved_context: list[dict[str, Any]],
        attempt: int,
    ) -> str:
        payload = {
            "request": request.model_dump(),
            "priority_signals": priority_signals,
            "retrieved_context": retrieved_context[:3],
            "candidate_recipe": candidate_recipe,
            "attempt": attempt,
        }
        return (
            "Generate one executable meal recommendation. "
            "Honor constraints, minimize grocery gap, prioritize expiring ingredients. "
            f"Payload: {json.dumps(payload, ensure_ascii=True)}"
        )

@lru_cache(maxsize=1)
def get_railtracks_workflow() -> RailtracksAgenticWorkflow:
    """Return cached Railtracks workflow instance."""
    return RailtracksAgenticWorkflow(get_settings())

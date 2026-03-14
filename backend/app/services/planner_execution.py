"""Shared planner execution flow for recommendation generation and persistence."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.agents.io_contracts import AgentPlanInputV1
from app.agents.rt_workflow import get_railtracks_workflow
from app.agents.tools import decompose_cooking_workflow, schedule_proactive_prep, sync_to_calendar
from app.models.plan_run import PlanRun
from app.models.recommendation import Recommendation
from app.schemas.contracts import ExecutionPlanBlock, PlanRequest
from app.services.user_memory import (
    count_expiring_items_used,
    infer_used_inventory,
    update_memory_after_recommendation,
)


async def execute_plan_request(
    *,
    db: Session,
    request: PlanRequest,
    trigger: str,
) -> Recommendation:
    """Run Railtracks planner workflow and persist Recommendation + PlanRun."""

    run = PlanRun(
        user_id=request.user_id,
        status="PROCESSING",
        mode="railtracks-agentic",
        request_payload=request.model_dump(),
        trace_notes=[f"trigger:{trigger}"],
    )
    db.add(run)
    db.flush()

    try:
        workflow = get_railtracks_workflow()
        agent_input = AgentPlanInputV1.from_plan_request(request)
        recommendation = await workflow.recommend_async(agent_input)

        rec = Recommendation(
            user_id=request.user_id,
            recipe_title=recommendation.decision.recipe_title,
            steps=recommendation.meal_plan.steps,
            nutrition_summary=recommendation.meal_plan.nutrition_summary.model_dump(),
            substitutions=recommendation.meal_plan.substitutions,
            spoilage_alerts=recommendation.meal_plan.spoilage_alerts,
            grocery_gap=[item.model_dump() for item in recommendation.grocery_plan.optimized_grocery_list],
            recipe_metadata={
                "source": "railtracks-agentic",
                "recipe_title": recommendation.decision.recipe_title,
                "recipe_id": None,
                "category": None,
                "area": None,
                "tags": [],
                "thumbnail_url": None,
                "youtube_url": None,
                "source_url": None,
                "ingredient_details": [],
                "api_source": "railtracks",
                "decision_rationale": recommendation.decision.rationale,
                "confidence": recommendation.decision.confidence,
            },
        )
        db.add(rec)
        db.flush()

        # Default auto-triggered execution tools (local persistence).
        dag_tasks_payload = decompose_cooking_workflow(recipe_id=rec.id, steps=recommendation.meal_plan.steps)
        prep_windows_payload = schedule_proactive_prep(
            task_list=dag_tasks_payload,
            user_availability={"anchor_iso": datetime.now(timezone.utc).isoformat()},
        )
        execution_payload = sync_to_calendar(
            user_id=request.user_id,
            recommendation_id=rec.id,
            recipe_title=recommendation.decision.recipe_title,
            cooking_dag_tasks=dag_tasks_payload,
            proactive_prep_windows=prep_windows_payload,
        )
        recommendation.execution_plan = ExecutionPlanBlock.model_validate(execution_payload)

        used_inventory = infer_used_inventory(
            request.inventory,
            recommendation.meal_plan.steps,
            recommendation.decision.recipe_title,
        )
        expiring_items_used = count_expiring_items_used(request.inventory, used_inventory)
        long_term_delta = update_memory_after_recommendation(
            db=db,
            user_id=request.user_id,
            recipe_title=recommendation.decision.recipe_title,
            used_inventory=used_inventory,
            grocery_gap=[item.ingredient for item in recommendation.grocery_plan.optimized_grocery_list],
            spoilage_alerts_count=len(recommendation.meal_plan.spoilage_alerts),
            expiring_items_used=expiring_items_used,
        )
        recommendation.memory_updates.long_term_metric_deltas = long_term_delta

        bundle_v1 = recommendation.to_recommendation_bundle(rec.id)
        recipe_metadata = dict(rec.recipe_metadata or {})
        recipe_metadata["execution_plan"] = recommendation.execution_plan.model_dump(mode="json")
        recipe_metadata["reflection"] = recommendation.reflection.model_dump(mode="json")
        recipe_metadata["memory_updates"] = recommendation.memory_updates.model_dump(mode="json")
        recipe_metadata["bundle_v1"] = bundle_v1.model_dump(mode="json")
        rec.recipe_metadata = recipe_metadata
        db.add(rec)

        run.status = "COMPLETED"
        run.mode = recommendation.mode
        run.recommendation_id = rec.id
        run.response_payload = bundle_v1.model_dump(mode="json")
        run.trace_notes = run.trace_notes + recommendation.trace_notes
        run.completed_at = datetime.now(timezone.utc)
        db.add(run)

        db.commit()
        db.refresh(rec)
        return rec
    except Exception as exc:
        db.rollback()
        failed_run = db.get(PlanRun, run.id)
        if failed_run:
            failed_run.status = "FAILED"
            failed_run.trace_notes = failed_run.trace_notes + [f"planner_exception:{exc.__class__.__name__}"]
            failed_run.completed_at = datetime.now(timezone.utc)
            db.add(failed_run)
            db.commit()
        raise

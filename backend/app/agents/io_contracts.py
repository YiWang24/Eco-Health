"""Canonical V1 agent input/output contracts and adapter helpers."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.contracts import (
    ConstraintSet,
    DecisionBlock,
    ExecutionPlanBlock,
    GroceryPlanBlock,
    InventorySnapshot,
    MealLog,
    MealPlanBlock,
    MemoryUpdatesBlock,
    PlanRequest,
    RecommendationBundle,
    ReflectionBlock,
)


class AgentPlanInputV1(BaseModel):
    """Stable adapter contract for agent execution inputs."""

    version: Literal["v1"] = "v1"
    user_id: str
    constraints: ConstraintSet
    inventory: InventorySnapshot | None = None
    latest_meal_log: MealLog | None = None
    user_message: str | None = None
    prior_recipe_hint: dict | None = None

    @classmethod
    def from_plan_request(cls, request: PlanRequest) -> "AgentPlanInputV1":
        return cls(
            user_id=request.user_id,
            constraints=request.constraints,
            inventory=request.inventory,
            latest_meal_log=request.latest_meal_log,
            user_message=request.user_message,
            prior_recipe_hint=request.prior_recipe_hint,
        )

    def to_plan_request(self) -> PlanRequest:
        return PlanRequest(
            user_id=self.user_id,
            constraints=self.constraints,
            inventory=self.inventory,
            latest_meal_log=self.latest_meal_log,
            user_message=self.user_message,
            prior_recipe_hint=self.prior_recipe_hint,
        )


class AgentPlanOutputV1(BaseModel):
    """Stable adapter contract for agent execution outputs."""

    version: Literal["v1"] = "v1"
    decision: DecisionBlock
    meal_plan: MealPlanBlock
    grocery_plan: GroceryPlanBlock
    execution_plan: ExecutionPlanBlock
    reflection: ReflectionBlock
    memory_updates: MemoryUpdatesBlock
    trace_notes: list[str] = Field(default_factory=list)
    mode: str = "railtracks"

    def to_recommendation_bundle(self, recommendation_id: str) -> RecommendationBundle:
        return RecommendationBundle(
            recommendation_id=recommendation_id,
            decision=self.decision,
            meal_plan=self.meal_plan,
            grocery_plan=self.grocery_plan,
            execution_plan=self.execution_plan,
            reflection=self.reflection,
            memory_updates=self.memory_updates,
        )

    @classmethod
    def from_recommendation_bundle(
        cls,
        bundle: RecommendationBundle,
        *,
        trace_notes: list[str] | None = None,
        mode: str = "railtracks",
    ) -> "AgentPlanOutputV1":
        return cls(
            decision=bundle.decision,
            meal_plan=bundle.meal_plan,
            grocery_plan=bundle.grocery_plan,
            execution_plan=bundle.execution_plan,
            reflection=bundle.reflection,
            memory_updates=bundle.memory_updates,
            trace_notes=trace_notes or [],
            mode=mode,
        )

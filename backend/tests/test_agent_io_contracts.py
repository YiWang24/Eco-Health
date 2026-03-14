"""Unit tests for stable V1 agent IO contracts."""

from app.agents.io_contracts import AgentPlanInputV1, AgentPlanOutputV1
from app.schemas.contracts import (
    DecisionBlock,
    ExecutionPlanBlock,
    GroceryItem,
    GroceryPlanBlock,
    MealPlanBlock,
    MemoryUpdatesBlock,
    NutritionSummary,
    PlanRequest,
    RecommendationBundle,
    ReflectionBlock,
)


def test_agent_input_roundtrip_plan_request_v1() -> None:
    request = PlanRequest(
        user_id="agent-io-user",
        constraints={
            "calories_target": 500,
            "dietary_restrictions": ["vegetarian"],
            "allergies": ["peanut"],
        },
        user_message="Use expiring ingredients first",
    )

    agent_input = AgentPlanInputV1.from_plan_request(request)
    restored = agent_input.to_plan_request()

    assert agent_input.version == "v1"
    assert restored.user_id == request.user_id
    assert restored.constraints.calories_target == 500
    assert restored.constraints.allergies == ["peanut"]
    assert restored.user_message == "Use expiring ingredients first"


def test_agent_output_roundtrip_recommendation_bundle_v1() -> None:
    grocery = [GroceryItem(ingredient="ginger", reason="required by selected recipe")]
    bundle = RecommendationBundle(
        recommendation_id="original-id",
        decision=DecisionBlock(recipe_title="Tofu Stir Fry", rationale="High pantry overlap", confidence=0.82),
        meal_plan=MealPlanBlock(
            steps=["Prep", "Cook", "Serve"],
            nutrition_summary=NutritionSummary(calories=420, protein_g=24, carbs_g=30, fat_g=14),
            substitutions=["Use tempeh instead of tofu"],
            spoilage_alerts=["Use spinach within 48h"],
        ),
        grocery_plan=GroceryPlanBlock(
            missing_ingredients=grocery,
            optimized_grocery_list=grocery,
            estimated_gap_cost=2.0,
        ),
        execution_plan=ExecutionPlanBlock(),
        reflection=ReflectionBlock(status="ok", attempts=1, violations=[], adjustments=[]),
        memory_updates=MemoryUpdatesBlock(short_term_updates=["inventory_loaded"], long_term_metric_deltas={}),
    )

    agent_output = AgentPlanOutputV1.from_recommendation_bundle(
        bundle,
        trace_notes=["workflow:railtracks-agentic"],
    )
    converted = agent_output.to_recommendation_bundle("new-rec-id")

    assert agent_output.version == "v1"
    assert agent_output.trace_notes == ["workflow:railtracks-agentic"]
    assert converted.recommendation_id == "new-rec-id"
    assert converted.decision.recipe_title == "Tofu Stir Fry"
    assert converted.meal_plan.nutrition_summary.calories == 420
    assert converted.grocery_plan.missing_ingredients[0].ingredient == "ginger"

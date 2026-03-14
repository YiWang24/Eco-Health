"""Tests for stage-based Railtracks workflow behavior."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.agents.io_contracts import AgentPlanInputV1
from app.agents.rt_workflow import RailtracksAgenticWorkflow
from app.agents.schemas import RtGroceryItem, RtNutritionSummary, RtRecommendationOutput
from app.schemas.contracts import ConstraintSet, InventoryItem, InventorySnapshot, PlanRequest


def _sample_request(user_id: str = "rt-user-1") -> AgentPlanInputV1:
    return AgentPlanInputV1.from_plan_request(
        PlanRequest(
            user_id=user_id,
            constraints=ConstraintSet(calories_target=500, allergies=["peanut"]),
            inventory=InventorySnapshot(
                user_id=user_id,
                items=[
                    InventoryItem(ingredient="spinach", quantity="1 bunch", expires_in_days=1),
                    InventoryItem(ingredient="tofu", quantity="400g", expires_in_days=2),
                ],
            ),
            user_message="Use expiring ingredients",
        )
    )


def _mock_rt_output() -> RtRecommendationOutput:
    return RtRecommendationOutput(
        recipe_title="Tofu Spinach Stir-Fry",
        steps=["Press tofu", "Chop vegetables", "Stir-fry together"],
        substitutions=["Swap spinach for kale"],
        spoilage_alerts=["Use spinach soon"],
        grocery_gap=[
            RtGroceryItem(ingredient="soy sauce", reason="required for sauce"),
            RtGroceryItem(ingredient="ginger", reason="for flavor"),
        ],
        nutrition_summary=RtNutritionSummary(calories=420, protein_g=22, carbs_g=18, fat_g=28),
        rationale="Good pantry overlap",
        confidence=0.84,
        confidence_note="High confidence match for inventory",
    )


def test_parse_valid_json_output() -> None:
    content = _mock_rt_output().model_dump_json()
    parsed = RailtracksAgenticWorkflow._parse_railtracks_output(content)
    assert parsed.recipe_title == "Tofu Spinach Stir-Fry"
    assert len(parsed.steps) == 3


def test_parse_invalid_json_raises_error() -> None:
    with pytest.raises(ValueError, match="Unable to parse Railtracks JSON output"):
        RailtracksAgenticWorkflow._parse_railtracks_output("No JSON here")


def test_recommend_async_raises_when_disabled() -> None:
    request = _sample_request()
    settings = MagicMock()
    settings.railtracks_enabled = False
    settings.openai_api_key = ""
    settings.railtracks_model = ""

    workflow = RailtracksAgenticWorkflow(settings)
    with pytest.raises(RuntimeError, match="disabled or unavailable"):
        asyncio.run(workflow.recommend_async(request))


def test_recommend_async_uses_agent_when_enabled() -> None:
    request = _sample_request()
    settings = MagicMock()
    settings.railtracks_enabled = True
    settings.openai_api_key = "test-key"
    settings.railtracks_model = "gpt-4o-mini"

    with patch("app.agents.rt_workflow.get_llm", return_value=MagicMock()):
        with patch("app.agents.rt_workflow.get_vector_store", return_value=MagicMock()):
            with patch.object(RailtracksAgenticWorkflow, "_build_agent", return_value=MagicMock()):
                workflow = RailtracksAgenticWorkflow(settings)

    mock_agent = MagicMock()
    mock_result = MagicMock()
    mock_result.content = _mock_rt_output().model_dump_json()
    mock_agent.run_async = AsyncMock(return_value=mock_result)
    workflow._agent = mock_agent

    output = asyncio.run(workflow.recommend_async(request))
    assert output.mode == "railtracks-agentic"
    assert output.decision.recipe_title == "Tofu Spinach Stir-Fry"
    assert any(note == "stage:PERCEIVE" for note in output.trace_notes)
    assert any(note.startswith("attempt:") for note in output.trace_notes)
    mock_agent.run_async.assert_called()


def test_recommend_async_raises_on_agent_error() -> None:
    request = _sample_request()
    settings = MagicMock()
    settings.railtracks_enabled = True
    settings.openai_api_key = "test-key"
    settings.railtracks_model = "gpt-4o-mini"

    with patch("app.agents.rt_workflow.get_llm", return_value=MagicMock()):
        with patch("app.agents.rt_workflow.get_vector_store", return_value=MagicMock()):
            with patch.object(RailtracksAgenticWorkflow, "_build_agent", return_value=MagicMock()):
                workflow = RailtracksAgenticWorkflow(settings)

    mock_agent = MagicMock()
    mock_agent.run_async = AsyncMock(side_effect=RuntimeError("Agent failed"))
    workflow._agent = mock_agent

    with pytest.raises(RuntimeError, match="Agent failed"):
        asyncio.run(workflow.recommend_async(request))

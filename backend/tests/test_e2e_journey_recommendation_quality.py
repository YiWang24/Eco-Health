"""Journey-oriented E2E tests for recommendation quality and personalization."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_e2e_09_actionable_recommendation_bundle(client: TestClient, auth_headers) -> None:
    """E2E-09: recommendation includes actionable fields."""

    user_id = "journey-plan-1"
    headers = auth_headers(user_id)

    response = client.post(
        "/api/v1/planner/recommendations",
        json={
            "user_id": user_id,
            "constraints": {"calories_target": 500, "dietary_restrictions": ["vegetarian"]},
            "inventory": {
                "user_id": user_id,
                "items": [{"ingredient": "spinach", "quantity": "1 bunch", "expires_in_days": 1}],
            },
        },
        headers=headers,
    )
    assert response.status_code == 200
    body = response.json()

    assert body["decision"]["recipe_title"]
    assert len(body["meal_plan"]["steps"]) >= 1
    assert "calories" in body["meal_plan"]["nutrition_summary"]
    assert isinstance(body["meal_plan"]["substitutions"], list)
    assert isinstance(body["meal_plan"]["spoilage_alerts"], list)
    assert isinstance(body["grocery_plan"]["missing_ingredients"], list)
    assert isinstance(body["execution_plan"]["cooking_dag_tasks"], list)
    assert "status" in body["reflection"]


def test_e2e_11_12_goal_and_lifestyle_constraints_influence_output(
    client: TestClient,
    auth_headers,
) -> None:
    """E2E-11/12: goal and lifestyle constraints change recommendation guidance."""

    user_id = "journey-plan-2"
    headers = auth_headers(user_id)

    weight_loss = client.post(
        "/api/v1/planner/recommendations",
        json={
            "user_id": user_id,
            "constraints": {
                "calories_target": 420,
                "dietary_restrictions": ["vegetarian"],
                "max_cook_time_minutes": 15,
            },
        },
        headers=headers,
    )
    assert weight_loss.status_code == 200

    high_protein = client.post(
        "/api/v1/planner/recommendations",
        json={
            "user_id": user_id,
            "constraints": {
                "protein_g_target": 40,
                "dietary_restrictions": ["vegetarian"],
                "max_cook_time_minutes": 30,
            },
        },
        headers=headers,
    )
    assert high_protein.status_code == 200

    low_cal_subs = set(weight_loss.json()["meal_plan"]["substitutions"])
    high_protein_subs = set(high_protein.json()["meal_plan"]["substitutions"])

    assert low_cal_subs != high_protein_subs
    assert any("calorie" in item.lower() for item in low_cal_subs)
    assert any("protein" in item.lower() for item in high_protein_subs)

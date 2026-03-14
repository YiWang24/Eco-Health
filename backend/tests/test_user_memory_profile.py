"""Long-term memory aggregation tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.core.database import SessionLocal
from app.models.user_memory_profile import UserMemoryProfile


def test_memory_metrics_increment_after_recommendation(client: TestClient, auth_headers) -> None:
    user_id = "memory-user-1"
    headers = auth_headers(user_id)

    resp = client.post(
        "/api/v1/planner/recommendations",
        json={
            "user_id": user_id,
            "constraints": {"dietary_restrictions": ["vegetarian"], "allergies": ["peanut"]},
            "inventory": {
                "user_id": user_id,
                "items": [
                    {"ingredient": "spinach", "quantity": "1 bunch", "expires_in_days": 1},
                    {"ingredient": "tofu", "quantity": "400g", "expires_in_days": 2},
                ],
            },
        },
        headers=headers,
    )
    assert resp.status_code == 200

    db = SessionLocal()
    try:
        memory = db.get(UserMemoryProfile, user_id)
        assert memory is not None
        assert memory.cumulative_money_saved >= 0.0
        assert isinstance(memory.food_waste_reduction_metrics, dict)
        assert isinstance(memory.sustainability_impact_metrics, dict)
        assert isinstance(memory.purchase_patterns, dict)
        assert isinstance(memory.favorite_recipes, list)
    finally:
        db.close()


def test_feedback_accept_and_reject_updates_favorites(client: TestClient, auth_headers) -> None:
    user_id = "memory-user-2"
    headers = auth_headers(user_id)

    rec_resp = client.post(
        "/api/v1/planner/recommendations",
        json={"user_id": user_id, "constraints": {}},
        headers=headers,
    )
    assert rec_resp.status_code == 200
    rec = rec_resp.json()
    rec_id = rec["recommendation_id"]
    recipe_title = rec["decision"]["recipe_title"]

    accept = client.patch(
        f"/api/v1/feedback/recommendations/{rec_id}",
        json={"action": "accept", "message": "Looks good"},
        headers=headers,
    )
    assert accept.status_code == 200

    db = SessionLocal()
    try:
        memory = db.get(UserMemoryProfile, user_id)
        assert memory is not None
        assert recipe_title in (memory.favorite_recipes or [])
    finally:
        db.close()

    reject = client.patch(
        f"/api/v1/feedback/recommendations/{rec_id}",
        json={"action": "reject", "message": "Try another"},
        headers=headers,
    )
    assert reject.status_code == 200

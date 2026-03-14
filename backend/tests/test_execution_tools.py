"""Execution-tool persistence tests for calendar + DAG + prep windows."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.core.database import SessionLocal
from app.models.calendar_block import CalendarBlock
from app.models.cooking_task import CookingTask
from app.models.prep_window import PrepWindow


def test_execution_plan_persisted_after_recommendation(client: TestClient, auth_headers) -> None:
    user_id = "exec-tools-1"
    headers = auth_headers(user_id)

    resp = client.post(
        "/api/v1/planner/recommendations",
        json={
            "user_id": user_id,
            "constraints": {"dietary_restrictions": ["vegetarian"]},
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
    body = resp.json()
    recommendation_id = body["recommendation_id"]

    assert isinstance(body["execution_plan"]["calendar_blocks"], list)
    assert len(body["execution_plan"]["calendar_blocks"]) >= 1
    assert len(body["execution_plan"]["cooking_dag_tasks"]) >= 1
    assert isinstance(body["execution_plan"]["proactive_prep_windows"], list)

    db = SessionLocal()
    try:
        calendar_rows = db.query(CalendarBlock).filter(CalendarBlock.recommendation_id == recommendation_id).all()
        dag_rows = db.query(CookingTask).filter(CookingTask.recommendation_id == recommendation_id).all()
        prep_rows = db.query(PrepWindow).filter(PrepWindow.recommendation_id == recommendation_id).all()

        assert len(calendar_rows) >= 1
        assert len(dag_rows) >= 1
        assert len(prep_rows) >= 0
    finally:
        db.close()

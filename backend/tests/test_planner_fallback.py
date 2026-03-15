"""Tests for offline fallback recommendation behavior."""

from fastapi.testclient import TestClient


def test_planner_uses_fallback_when_workflow_unavailable(
    client: TestClient,
    auth_headers,
    monkeypatch,
) -> None:
    class _BrokenWorkflow:
        async def recommend_async(self, _request):
            raise RuntimeError("Railtracks workflow is disabled or unavailable")

    monkeypatch.setattr("app.services.planner_execution.get_railtracks_workflow", lambda: _BrokenWorkflow())

    user_id = "fallback-user-1"
    headers = auth_headers(user_id)
    payload = {"user_id": user_id, "constraints": {"calories_target": 1800}}

    response = client.post("/api/v1/planner/recommendations", json=payload, headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["decision"]["recipe_title"]
    assert body["reflection"]["status"] == "fallback"

    latest_run = client.get(f"/api/v1/planner/runs/latest/{user_id}", headers=headers)
    assert latest_run.status_code == 200
    assert "fallback:RuntimeError" in latest_run.json()["trace_notes"]

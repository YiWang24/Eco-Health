"""Tests for recommendation retrieval views used by frontend pages."""

from fastapi.testclient import TestClient


def _create_recommendation(client: TestClient, headers: dict[str, str], user_id: str) -> str:
    response = client.post(
        "/api/v1/planner/recommendations",
        json={"user_id": user_id, "constraints": {}},
        headers=headers,
    )
    assert response.status_code == 200
    return response.json()["recommendation_id"]


def test_recommendation_history_returns_latest_first(client: TestClient, auth_headers) -> None:
    user_id = "history-user-1"
    headers = auth_headers(user_id)

    first_id = _create_recommendation(client, headers, user_id)
    second_id = _create_recommendation(client, headers, user_id)

    response = client.get(f"/api/v1/planner/recommendations/history/{user_id}?limit=10", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert len(body) >= 2
    assert body[0]["recommendation_id"] == second_id
    assert body[1]["recommendation_id"] == first_id


def test_get_recommendation_by_id_returns_bundle(client: TestClient, auth_headers) -> None:
    user_id = "history-user-2"
    headers = auth_headers(user_id)

    recommendation_id = _create_recommendation(client, headers, user_id)
    response = client.get(f"/api/v1/planner/recommendations/{recommendation_id}", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["recommendation_id"] == recommendation_id
    assert body["decision"]["recipe_title"]

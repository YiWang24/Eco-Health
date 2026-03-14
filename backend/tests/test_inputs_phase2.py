"""Tests for phase-2 input ingestion and background processing."""

import time

from fastapi.testclient import TestClient

def _poll_job(client: TestClient, job_id: str, headers: dict[str, str]) -> dict:
    for _ in range(12):
        response = client.get(f"/api/v1/inputs/jobs/{job_id}", headers=headers)
        assert response.status_code == 200
        body = response.json()
        if body["status"] == "COMPLETED":
            return body
        time.sleep(0.05)
    return body


def test_fridge_scan_requires_auth(client: TestClient) -> None:
    response = client.post("/api/v1/inputs/fridge-scan", json={"image_url": "https://example.com/fridge.jpg"})

    assert response.status_code == 401


def test_fridge_scan_creates_job_and_completes(client: TestClient) -> None:
    headers = {"Authorization": "Bearer fake-token", "X-Test-User-Id": "user-input-1"}

    created = client.post("/api/v1/inputs/fridge-scan", json={"image_url": "https://example.com/fridge.jpg"}, headers=headers)
    assert created.status_code == 202
    created_body = created.json()
    assert "job_id" in created_body

    completed = _poll_job(client, created_body["job_id"], headers)
    assert completed["status"] == "COMPLETED"
    assert completed["result"]["input_type"] == "fridge_scan"
    assert completed["result"]["updated_items"] >= 1


def test_meal_scan_creates_job_and_meal_log_result(client: TestClient) -> None:
    headers = {"Authorization": "Bearer fake-token", "X-Test-User-Id": "user-input-2"}

    created = client.post("/api/v1/inputs/meal-scan", json={"image_url": "https://example.com/meal.jpg"}, headers=headers)
    assert created.status_code == 202

    completed = _poll_job(client, created.json()["job_id"], headers)
    assert completed["status"] == "COMPLETED"
    assert completed["result"]["input_type"] == "meal_scan"
    assert completed["result"]["meal_logged"] is True


def test_chat_message_persists_event(client: TestClient) -> None:
    headers = {"Authorization": "Bearer fake-token", "X-Test-User-Id": "user-input-3"}

    response = client.post(
        "/api/v1/inputs/chat-message",
        json={"message": "Make it vegetarian and under 500 calories"},
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == "user-input-3"
    assert body["message"] == "Make it vegetarian and under 500 calories"
    assert body["event_id"]

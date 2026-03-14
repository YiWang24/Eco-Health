"""Tests for phase-1 profile and goals behaviors."""

from fastapi.testclient import TestClient

def test_profile_requires_auth(client: TestClient) -> None:
    response = client.get("/api/v1/profiles/user-1")

    assert response.status_code == 401


def test_profile_put_then_get_roundtrip(client: TestClient) -> None:
    payload = {
        "age": 29,
        "height_cm": 171.5,
        "weight_kg": 63.2,
        "activity_level": "moderate",
        "dietary_preferences": ["vegetarian"],
        "allergies": ["peanut"],
        "cook_time_preference_minutes": 20,
    }
    headers = {"Authorization": "Bearer fake-token"}

    upsert = client.put("/api/v1/profiles/user-1", json=payload, headers=headers)
    assert upsert.status_code == 200
    assert upsert.json()["user_id"] == "user-1"
    assert upsert.json()["age"] == 29

    fetched = client.get("/api/v1/profiles/user-1", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["user_id"] == "user-1"
    assert fetched.json()["dietary_preferences"] == ["vegetarian"]


def test_goals_put_then_get_roundtrip(client: TestClient) -> None:
    payload = {
        "calories_target": 2100,
        "protein_g_target": 130,
        "carbs_g_target": 220,
        "fat_g_target": 70,
        "dietary_restrictions": ["vegetarian"],
        "allergies": ["peanut"],
        "budget_limit": 28.5,
        "max_cook_time_minutes": 25,
    }
    headers = {"Authorization": "Bearer fake-token"}

    upsert = client.put("/api/v1/goals/user-1", json=payload, headers=headers)
    assert upsert.status_code == 200
    assert upsert.json()["user_id"] == "user-1"
    assert upsert.json()["calories_target"] == 2100

    fetched = client.get("/api/v1/goals/user-1", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["user_id"] == "user-1"
    assert fetched.json()["max_cook_time_minutes"] == 25

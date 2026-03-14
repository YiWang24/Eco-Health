"""E2E tests for different input type combinations and pantry state building."""

from __future__ import annotations

import time

from fastapi.testclient import TestClient


def _headers(auth_headers, user_id: str) -> dict[str, str]:
    return auth_headers(user_id)


def _poll_job(client: TestClient, job_id: str, headers: dict) -> dict:
    for _ in range(20):
        resp = client.get(f"/api/v1/inputs/jobs/{job_id}", headers=headers)
        assert resp.status_code == 200
        body = resp.json()
        if body["status"] == "COMPLETED":
            return body
        time.sleep(0.05)
    return resp.json()


def _pantry(client: TestClient, headers: dict) -> list[dict]:
    resp = client.get("/api/v1/inputs/pantry", headers=headers)
    assert resp.status_code == 200
    return resp.json()


# ---------------------------------------------------------------------------
# Fridge-only
# ---------------------------------------------------------------------------

def test_fridge_scan_only_builds_pantry(client: TestClient, auth_headers) -> None:
    """E2E-03: fridge-only flow updates pantry state."""
    user_id = "ic-fridge-1"
    headers = _headers(auth_headers, user_id)

    resp = client.post(
        "/api/v1/inputs/fridge-scan",
        json={
            "image_url": "https://example.com/fridge_ic1.jpg",
            "detected_items": [
                {"ingredient": "kale", "quantity": "1 bag", "expires_in_days": 3},
                {"ingredient": "eggs", "quantity": "6", "expires_in_days": 14},
            ],
        },
        headers=headers,
    )
    assert resp.status_code == 202
    _poll_job(client, resp.json()["job_id"], headers)

    items = _pantry(client, headers)
    ingredients = {i["ingredient"].lower() for i in items}
    assert "kale" in ingredients
    assert "eggs" in ingredients


# ---------------------------------------------------------------------------
# Meal-only
# ---------------------------------------------------------------------------

def test_meal_scan_only_records_meal_log(client: TestClient, auth_headers) -> None:
    """E2E-05: meal scan creates meal log context."""
    user_id = "ic-meal-1"
    headers = _headers(auth_headers, user_id)

    resp = client.post(
        "/api/v1/inputs/meal-scan",
        json={
            "image_url": "https://example.com/meal_ic1.jpg",
            "meal_name": "Grilled Salmon",
            "calories": 400,
            "protein_g": 38,
            "carbs_g": 12,
            "fat_g": 18,
        },
        headers=headers,
    )
    assert resp.status_code == 202
    result = _poll_job(client, resp.json()["job_id"], headers)
    assert result["status"] == "COMPLETED"
    assert result["result"]["input_type"] == "meal_scan"
    assert result["result"]["meal_logged"] is True


# ---------------------------------------------------------------------------
# Receipt-only
# ---------------------------------------------------------------------------

def test_receipt_scan_only_adds_pantry_items(client: TestClient, auth_headers) -> None:
    """E2E-04: receipt-only flow updates pantry state."""
    user_id = "ic-receipt-1"
    headers = _headers(auth_headers, user_id)

    resp = client.post(
        "/api/v1/inputs/receipt-scan",
        json={
            "image_url": "https://example.com/receipt_ic1.jpg",
            "items": [
                {"ingredient": "chickpeas", "quantity": "400g", "expires_in_days": 730},
                {"ingredient": "olive oil", "quantity": "500ml", "expires_in_days": 365},
            ],
        },
        headers=headers,
    )
    assert resp.status_code == 202
    _poll_job(client, resp.json()["job_id"], headers)

    items = _pantry(client, headers)
    ingredients = {i["ingredient"].lower() for i in items}
    assert "chickpeas" in ingredients
    assert "olive oil" in ingredients


# ---------------------------------------------------------------------------
# Combined fridge + receipt
# ---------------------------------------------------------------------------

def test_fridge_plus_receipt_merges_pantry(client: TestClient, auth_headers) -> None:
    user_id = "ic-combo-1"
    headers = _headers(auth_headers, user_id)

    fridge_resp = client.post(
        "/api/v1/inputs/fridge-scan",
        json={
            "image_url": "https://example.com/fridge_combo.jpg",
            "detected_items": [
                {"ingredient": "yogurt", "quantity": "500g", "expires_in_days": 5},
            ],
        },
        headers=headers,
    )
    assert fridge_resp.status_code == 202
    _poll_job(client, fridge_resp.json()["job_id"], headers)

    receipt_resp = client.post(
        "/api/v1/inputs/receipt-scan",
        json={
            "image_url": "https://example.com/receipt_combo.jpg",
            "items": [
                {"ingredient": "oats", "quantity": "1kg", "expires_in_days": 180},
            ],
        },
        headers=headers,
    )
    assert receipt_resp.status_code == 202
    _poll_job(client, receipt_resp.json()["job_id"], headers)

    items = _pantry(client, headers)
    ingredients = {i["ingredient"].lower() for i in items}
    assert "yogurt" in ingredients
    assert "oats" in ingredients


def test_combined_scan_planner_uses_context(client: TestClient, auth_headers) -> None:
    """E2E-07: planner autofills inventory from persisted pantry context."""
    user_id = "ic-combo-2"
    headers = _headers(auth_headers, user_id)

    # Seed pantry
    fridge = client.post(
        "/api/v1/inputs/fridge-scan",
        json={
            "image_url": "https://example.com/fridge_combo2.jpg",
            "detected_items": [
                {"ingredient": "tofu", "quantity": "400g", "expires_in_days": 2},
            ],
        },
        headers=headers,
    )
    _poll_job(client, fridge.json()["job_id"], headers)

    # Plan with empty inventory — should pick up from pantry
    plan_resp = client.post(
        "/api/v1/planner/recommendations",
        json={
            "user_id": user_id,
            "constraints": {"dietary_restrictions": ["vegetarian"]},
        },
        headers=headers,
    )
    assert plan_resp.status_code == 200
    body = plan_resp.json()
    assert body["recommendation_id"]
    assert body["decision"]["recipe_title"]

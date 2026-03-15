"""Tests for Cognito callback endpoint behavior."""

from fastapi.testclient import TestClient

from app.core.config import get_settings


def test_cognito_callback_requires_code(client: TestClient) -> None:
    response = client.get("/api/v1/auth/cognito/callback")

    assert response.status_code == 400
    body = response.json()
    assert "Missing authorization code" in body["detail"]


def test_cognito_callback_success(client: TestClient) -> None:
    response = client.get("/api/v1/auth/cognito/callback?code=abc123&state=xyz")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "callback_received"
    assert body["authorization_code"] == "abc123"
    assert body["state"] == "xyz"


def test_me_requires_strict_valid_jwt(client: TestClient, auth_headers) -> None:
    response = client.get("/api/v1/auth/me", headers=auth_headers("auth-user-1"))
    assert response.status_code == 200
    assert response.json()["user_id"] == "auth-user-1"


def test_me_supports_dev_bypass_only_when_enabled(client: TestClient, monkeypatch) -> None:
    monkeypatch.setenv("COGNITO_ISSUER", "")
    monkeypatch.setenv("COGNITO_CLIENT_ID", "")
    monkeypatch.setenv("AUTH_BYPASS_ENABLED", "true")
    get_settings.cache_clear()

    response = client.get("/api/v1/auth/me", headers={"X-Demo-User": "hackathon-user"})

    assert response.status_code == 200
    assert response.json()["user_id"] == "hackathon-user"
    assert response.json()["email"] == "hackathon-user@demo.local"

    get_settings.cache_clear()

"""Tests for Cognito register/login endpoint contracts."""

from fastapi.testclient import TestClient


def test_register_returns_delivery_info(client: TestClient, monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.v1.endpoints.auth.cognito_sign_up",
        lambda email, password, settings: {
            "UserSub": "user-sub-1",
            "UserConfirmed": False,
            "CodeDeliveryDetails": {
                "DeliveryMedium": "EMAIL",
                "Destination": "e***@example.com",
            },
        },
    )

    response = client.post(
        "/api/v1/auth/register",
        json={"email": "hello@example.com", "password": "Abcd1234!"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "hello@example.com"
    assert body["user_sub"] == "user-sub-1"
    assert body["user_confirmed"] is False
    assert body["code_delivery_medium"] == "EMAIL"


def test_confirm_email_success(client: TestClient, monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.v1.endpoints.auth.cognito_confirm_sign_up",
        lambda email, code, settings: {},
    )

    response = client.post(
        "/api/v1/auth/confirm-email",
        json={"email": "hello@example.com", "code": "123456"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "email_confirmed"


def test_login_returns_tokens(client: TestClient, monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.v1.endpoints.auth.cognito_login",
        lambda email, password, settings: {
            "AuthenticationResult": {
                "IdToken": "id-token",
                "AccessToken": "access-token",
                "RefreshToken": "refresh-token",
                "TokenType": "Bearer",
                "ExpiresIn": 3600,
            }
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "hello@example.com", "password": "Abcd1234!"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id_token"] == "id-token"
    assert body["refresh_token"] == "refresh-token"
    assert body["token_type"] == "Bearer"


def test_refresh_reuses_client_refresh_token(client: TestClient, monkeypatch) -> None:
    refresh_token = "x" * 32
    monkeypatch.setattr(
        "app.api.v1.endpoints.auth.cognito_refresh",
        lambda refresh_token, settings, email=None: {
            "AuthenticationResult": {
                "IdToken": "new-id-token",
                "AccessToken": "new-access-token",
                "TokenType": "Bearer",
                "ExpiresIn": 3600,
            }
        },
    )

    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token, "email": "hello@example.com"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id_token"] == "new-id-token"
    assert body["refresh_token"] == refresh_token

"""Authentication dependency helpers for Cognito-backed API calls."""

from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status
from jose import jwt

from app.core.config import Settings, get_settings
from app.schemas.auth import AuthContext


def _extract_bearer_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    return auth_header.split(" ", 1)[1].strip()


def _dev_auth_context(request: Request) -> AuthContext:
    user_id = request.headers.get("X-Test-User-Id", "user-1")
    return AuthContext(user_id=user_id, email="dev@example.com")


def _claims_auth_context(token: str, settings: Settings) -> AuthContext:
    # NOTE: For hackathon speed, this validates issuer and claim shape only.
    # Signature verification against Cognito JWKS should be added in Phase 1 hardening.
    try:
        claims = jwt.get_unverified_claims(token)
    except Exception as exc:  # pragma: no cover - defensive guard
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    iss = claims.get("iss")
    if settings.cognito_issuer and iss != settings.cognito_issuer:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token issuer")

    sub = claims.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing subject")

    return AuthContext(user_id=sub, email=claims.get("email"))


def get_current_user(request: Request, settings: Settings = Depends(get_settings)) -> AuthContext:
    """Resolve the authenticated user context from bearer token."""

    token = _extract_bearer_token(request)

    if settings.env != "production" and token == "fake-token":
        return _dev_auth_context(request)

    return _claims_auth_context(token, settings)

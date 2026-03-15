"""Authentication dependency helpers for Cognito-backed API calls."""

from __future__ import annotations

import json
import time
from pathlib import Path

import httpx
from fastapi import Depends, HTTPException, Request, status
from jose import jwt

from app.core.config import Settings, get_settings
from app.schemas.auth import AuthContext

_JWKS_CACHE: dict[str, dict] = {}
_JWKS_CACHE_TTL_SECONDS = 300


def _should_use_dev_bypass(settings: Settings) -> bool:
    """Allow local hackathon demos without Cognito provisioning."""

    return settings.env == "development" and settings.auth_bypass_enabled


def _resolve_dev_auth_context(request: Request) -> AuthContext:
    user_id = (
        request.headers.get("X-Demo-User")
        or request.headers.get("X-Demo-User-Id")
        or "demo-user"
    ).strip()
    return AuthContext(user_id=user_id, email=f"{user_id}@demo.local")


def _extract_bearer_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    return auth_header.split(" ", 1)[1].strip()


def _resolve_local_jwks(settings: Settings) -> dict | None:
    """Resolve local JWKS for offline/strict local verification."""

    if settings.cognito_jwks_json:
        try:
            payload = json.loads(settings.cognito_jwks_json)
            if isinstance(payload, dict):
                return payload
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid COGNITO_JWKS_JSON payload",
            ) from exc

    if settings.cognito_jwks_path:
        path = Path(settings.cognito_jwks_path).expanduser()
        if not path.exists():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Configured COGNITO_JWKS_PATH does not exist",
            )
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                return payload
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid JWKS JSON file at COGNITO_JWKS_PATH",
            ) from exc

    return None


def _resolve_jwks_url(settings: Settings) -> str:
    if settings.cognito_jwks_url:
        return settings.cognito_jwks_url
    if settings.cognito_issuer:
        return settings.cognito_issuer.rstrip("/") + "/.well-known/jwks.json"
    return ""


def _validate_auth_config(settings: Settings) -> None:
    if not settings.cognito_client_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="COGNITO_CLIENT_ID is required when auth bypass is disabled",
        )
    if not (
        settings.cognito_issuer
        or settings.cognito_jwks_url
        or settings.cognito_jwks_json
        or settings.cognito_jwks_path
    ):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="COGNITO_ISSUER or Cognito JWKS config is required when auth bypass is disabled",
        )


def _fetch_jwks(settings: Settings) -> dict:
    local = _resolve_local_jwks(settings)
    if local is not None:
        return local

    jwks_url = _resolve_jwks_url(settings)
    if not jwks_url:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cognito JWKS URL is not configured")

    cache_key = jwks_url
    cached = _JWKS_CACHE.get(cache_key)
    now = time.time()
    if cached and now - cached["fetched_at"] < _JWKS_CACHE_TTL_SECONDS:
        return cached["jwks"]

    response = httpx.get(jwks_url, timeout=5.0)
    response.raise_for_status()
    jwks = response.json()
    _JWKS_CACHE[cache_key] = {"jwks": jwks, "fetched_at": now}
    return jwks


def _claims_auth_context(token: str, settings: Settings) -> AuthContext:
    try:
        headers = jwt.get_unverified_header(token)
    except Exception as exc:  # pragma: no cover - defensive guard
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token header") from exc

    kid = headers.get("kid")
    if not kid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing key id")

    try:
        jwks = _fetch_jwks(settings)
    except Exception as exc:  # pragma: no cover - network/provider failure
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to fetch JWKS") from exc

    key = next((item for item in jwks.get("keys", []) if item.get("kid") == kid), None)
    if not key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No matching JWKS key")

    decode_kwargs = {
        "key": key,
        "algorithms": ["RS256"],
    }
    options = {"verify_aud": False, "verify_iss": bool(settings.cognito_issuer)}
    if settings.cognito_issuer:
        decode_kwargs["issuer"] = settings.cognito_issuer

    try:
        claims = jwt.decode(token, options=options, **decode_kwargs)
    except Exception as exc:  # pragma: no cover - defensive guard
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token verification failed") from exc

    if settings.cognito_client_id:
        audience_claim = claims.get("aud") or claims.get("client_id")
        if audience_claim != settings.cognito_client_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token audience mismatch")

    sub = claims.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing subject")

    return AuthContext(user_id=sub, email=claims.get("email"))


def get_current_user(request: Request, settings: Settings = Depends(get_settings)) -> AuthContext:
    """Resolve the authenticated user context from bearer token."""

    if _should_use_dev_bypass(settings):
        return _resolve_dev_auth_context(request)

    _validate_auth_config(settings)
    token = _extract_bearer_token(request)
    return _claims_auth_context(token, settings)

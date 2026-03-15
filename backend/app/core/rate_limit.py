"""Global daily request rate limiter middleware."""

from __future__ import annotations

import threading
from datetime import date, timezone, datetime

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

DAILY_LIMIT = 5000

# Paths exempt from rate limiting (health/meta endpoints)
_EXEMPT_PREFIXES = (
    "/docs",
    "/redoc",
    "/openapi.json",
    "/api/v1/health",
)

_lock = threading.Lock()
_state: dict = {"date": None, "count": 0}


def _today() -> date:
    return datetime.now(tz=timezone.utc).date()


def _increment_and_check() -> tuple[int, bool]:
    """Atomically increment counter, resetting on a new UTC day.

    Returns (current_count, allowed).
    """
    with _lock:
        today = _today()
        if _state["date"] != today:
            _state["date"] = today
            _state["count"] = 0
        _state["count"] += 1
        count = _state["count"]
    return count, count <= DAILY_LIMIT


def get_daily_usage() -> dict:
    """Return current counter snapshot (for health/admin endpoints)."""
    with _lock:
        return {
            "date": str(_state["date"]),
            "count": _state["count"],
            "limit": DAILY_LIMIT,
            "remaining": max(0, DAILY_LIMIT - _state["count"]),
        }


class DailyRateLimitMiddleware(BaseHTTPMiddleware):
    """Reject requests once the global daily quota is exhausted."""

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(path.startswith(p) for p in _EXEMPT_PREFIXES):
            return await call_next(request)

        count, allowed = _increment_and_check()
        remaining = max(0, DAILY_LIMIT - count)

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Daily request limit reached. Service resets at midnight UTC.",
                    "limit": DAILY_LIMIT,
                    "remaining": 0,
                },
                headers={
                    "X-RateLimit-Limit": str(DAILY_LIMIT),
                    "X-RateLimit-Remaining": "0",
                    "Retry-After": "86400",
                },
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(DAILY_LIMIT)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response

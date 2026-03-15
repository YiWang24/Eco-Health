"""FastAPI application entrypoint."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.database import init_db, persist_sqlite_snapshot
from app.core.rate_limit import DailyRateLimitMiddleware

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")


def _parse_cors_origins(raw: str) -> list[str]:
    """Parse comma separated CORS origins from environment configuration."""

    origins = [item.strip() for item in raw.split(",") if item.strip()]
    if not origins:
        return ["http://localhost:3000"]
    return origins


app.add_middleware(
    CORSMiddleware,
    allow_origins=_parse_cors_origins(settings.cors_allowed_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(DailyRateLimitMiddleware)

app.include_router(api_router, prefix=settings.api_v1_str)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.on_event("shutdown")
def on_shutdown() -> None:
    persist_sqlite_snapshot()

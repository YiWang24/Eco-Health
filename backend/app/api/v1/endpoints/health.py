"""Health endpoint for runtime checks."""

from fastapi import APIRouter

from app.core.rate_limit import get_daily_usage

router = APIRouter(tags=["system"])


@router.get("/health")
async def health() -> dict:
    return {"status": "ok", "rate_limit": get_daily_usage()}

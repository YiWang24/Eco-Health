"""Authentication endpoints (Cognito integration placeholders)."""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/cognito/callback")
async def cognito_signup_callback() -> dict[str, str]:
    return {"status": "stub", "message": "Cognito callback mapping not implemented yet."}

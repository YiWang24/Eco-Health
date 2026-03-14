"""Authentication endpoints (Cognito integration placeholders)."""

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.schemas.auth import AuthContext

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/cognito/callback")
async def cognito_signup_callback() -> dict[str, str]:
    return {"status": "stub", "message": "Cognito callback mapping not implemented yet."}


@router.get("/me")
async def me(current_user: AuthContext = Depends(get_current_user)) -> AuthContext:
    return current_user

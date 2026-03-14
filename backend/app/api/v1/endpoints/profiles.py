"""Profile endpoints for onboarding and user context."""

from fastapi import APIRouter

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/{user_id}")
async def get_profile(user_id: str) -> dict[str, str]:
    return {"status": "stub", "message": f"Profile lookup for {user_id} is not implemented yet."}


@router.put("/{user_id}")
async def upsert_profile(user_id: str) -> dict[str, str]:
    return {"status": "stub", "message": f"Profile upsert for {user_id} is not implemented yet."}

"""Goal endpoints for nutrition targets and constraints."""

from fastapi import APIRouter

router = APIRouter(prefix="/goals", tags=["goals"])


@router.get("/{user_id}")
async def get_goals(user_id: str) -> dict[str, str]:
    return {"status": "stub", "message": f"Goals lookup for {user_id} is not implemented yet."}


@router.put("/{user_id}")
async def upsert_goals(user_id: str) -> dict[str, str]:
    return {"status": "stub", "message": f"Goals upsert for {user_id} is not implemented yet."}

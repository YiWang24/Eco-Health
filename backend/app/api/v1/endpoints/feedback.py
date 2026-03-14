"""Feedback endpoints for accept/reject and replan triggers."""

from fastapi import APIRouter

from app.schemas.contracts import FeedbackPatch

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.patch("/recommendations/{recommendation_id}")
async def patch_recommendation_feedback(recommendation_id: str, payload: FeedbackPatch) -> dict[str, str]:
    return {
        "status": "stub",
        "message": (
            f"Feedback '{payload.action}' for recommendation {recommendation_id} is not implemented yet."
        ),
    }

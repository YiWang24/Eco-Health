"""Planning endpoints for recommendation generation and retrieval."""

from fastapi import APIRouter

from app.schemas.contracts import PlanRequest

router = APIRouter(prefix="/planner", tags=["planner"])


@router.post("/recommendations")
async def create_recommendation(request: PlanRequest) -> dict[str, str]:
    return {
        "status": "stub",
        "message": f"Plan generation for user {request.user_id} is not implemented yet.",
    }


@router.post("/recommendations/{recommendation_id}/replan")
async def replan_recommendation(recommendation_id: str) -> dict[str, str]:
    return {
        "status": "stub",
        "message": f"Replan for recommendation {recommendation_id} is not implemented yet.",
    }


@router.get("/recommendations/latest/{user_id}")
async def get_latest_recommendation(user_id: str) -> dict[str, str]:
    return {
        "status": "stub",
        "message": f"Latest recommendation for user {user_id} is not implemented yet.",
    }


@router.get("/recommendations/{recommendation_id}/recipe")
async def get_recipe_detail(recommendation_id: str) -> dict[str, str]:
    return {
        "status": "stub",
        "message": f"Recipe detail for recommendation {recommendation_id} is not implemented yet.",
    }


@router.get("/recommendations/{recommendation_id}/nutrition")
async def get_nutrition_summary(recommendation_id: str) -> dict[str, str]:
    return {
        "status": "stub",
        "message": f"Nutrition summary for recommendation {recommendation_id} is not implemented yet.",
    }


@router.get("/recommendations/{recommendation_id}/grocery-gap")
async def get_grocery_gap(recommendation_id: str) -> dict[str, str]:
    return {
        "status": "stub",
        "message": f"Grocery gap for recommendation {recommendation_id} is not implemented yet.",
    }

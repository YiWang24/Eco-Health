"""Goal endpoints for nutrition targets and constraints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.goal import Goal
from app.schemas.auth import AuthContext
from app.schemas.goal import GoalResponse, GoalUpsert
from app.services.user_context import ensure_user

router = APIRouter(prefix="/goals", tags=["goals"])


@router.get("/{user_id}", response_model=GoalResponse)
async def get_goals(
    user_id: str,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GoalResponse:
    ensure_user(db, current_user)
    if user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden user scope")

    goal = db.get(Goal, user_id)
    if not goal:
        return GoalResponse(user_id=user_id)

    return GoalResponse(
        user_id=goal.user_id,
        calories_target=goal.calories_target,
        protein_g_target=goal.protein_g_target,
        carbs_g_target=goal.carbs_g_target,
        fat_g_target=goal.fat_g_target,
        dietary_restrictions=goal.dietary_restrictions or [],
        allergies=goal.allergies or [],
        budget_limit=goal.budget_limit,
        max_cook_time_minutes=goal.max_cook_time_minutes,
    )


@router.put("/{user_id}", response_model=GoalResponse)
async def upsert_goals(
    user_id: str,
    payload: GoalUpsert,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GoalResponse:
    ensure_user(db, current_user)
    if user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden user scope")

    goal = db.get(Goal, user_id)
    if not goal:
        goal = Goal(user_id=user_id)

    goal.calories_target = payload.calories_target
    goal.protein_g_target = payload.protein_g_target
    goal.carbs_g_target = payload.carbs_g_target
    goal.fat_g_target = payload.fat_g_target
    goal.dietary_restrictions = payload.dietary_restrictions
    goal.allergies = payload.allergies
    goal.budget_limit = payload.budget_limit
    goal.max_cook_time_minutes = payload.max_cook_time_minutes

    db.add(goal)
    db.commit()
    db.refresh(goal)

    return GoalResponse(
        user_id=goal.user_id,
        calories_target=goal.calories_target,
        protein_g_target=goal.protein_g_target,
        carbs_g_target=goal.carbs_g_target,
        fat_g_target=goal.fat_g_target,
        dietary_restrictions=goal.dietary_restrictions or [],
        allergies=goal.allergies or [],
        budget_limit=goal.budget_limit,
        max_cook_time_minutes=goal.max_cook_time_minutes,
    )

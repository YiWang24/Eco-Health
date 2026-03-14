"""Profile endpoints for onboarding and user context."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.profile import Profile
from app.schemas.auth import AuthContext
from app.schemas.profile import ProfileResponse, ProfileUpsert
from app.services.user_context import ensure_user

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/{user_id}", response_model=ProfileResponse)
async def get_profile(
    user_id: str,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfileResponse:
    ensure_user(db, current_user)
    if user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden user scope")

    profile = db.get(Profile, user_id)
    if not profile:
        return ProfileResponse(user_id=user_id)

    return ProfileResponse(
        user_id=profile.user_id,
        age=profile.age,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        activity_level=profile.activity_level,
        dietary_preferences=profile.dietary_preferences or [],
        allergies=profile.allergies or [],
        cook_time_preference_minutes=profile.cook_time_preference_minutes,
    )


@router.put("/{user_id}", response_model=ProfileResponse)
async def upsert_profile(
    user_id: str,
    payload: ProfileUpsert,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfileResponse:
    ensure_user(db, current_user)
    if user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden user scope")

    profile = db.get(Profile, user_id)
    if not profile:
        profile = Profile(user_id=user_id)

    profile.age = payload.age
    profile.height_cm = payload.height_cm
    profile.weight_kg = payload.weight_kg
    profile.activity_level = payload.activity_level
    profile.dietary_preferences = payload.dietary_preferences
    profile.allergies = payload.allergies
    profile.cook_time_preference_minutes = payload.cook_time_preference_minutes

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return ProfileResponse(
        user_id=profile.user_id,
        age=profile.age,
        height_cm=profile.height_cm,
        weight_kg=profile.weight_kg,
        activity_level=profile.activity_level,
        dietary_preferences=profile.dietary_preferences or [],
        allergies=profile.allergies or [],
        cook_time_preference_minutes=profile.cook_time_preference_minutes,
    )

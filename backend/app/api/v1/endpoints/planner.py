"""Planning endpoints for recommendation generation and retrieval."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.plan_run import PlanRun
from app.models.recommendation import Recommendation
from app.schemas.auth import AuthContext
from app.schemas.contracts import ConstraintSet, PlanRequest, RecommendationBundle, ReplanRequest
from app.services.constraint_parser import merge_constraints
from app.services.planner_execution import execute_plan_request
from app.services.planner_context import build_effective_plan_request
from app.services.recommendation_mapper import recommendation_to_bundle
from app.services.user_context import ensure_user

router = APIRouter(prefix="/planner", tags=["planner"])


def _to_bundle(rec: Recommendation) -> RecommendationBundle:
    return recommendation_to_bundle(rec)


def _load_constraints_from_recommendation_run(
    db: Session,
    recommendation_id: str,
) -> ConstraintSet | None:
    """Load effective constraints from the original recommendation run payload."""

    run = (
        db.execute(
            select(PlanRun)
            .where(PlanRun.recommendation_id == recommendation_id)
            .order_by(PlanRun.created_at.desc())
        )
        .scalars()
        .first()
    )
    if not run:
        return None

    payload = run.request_payload or {}
    constraints_payload = payload.get("constraints")
    if not isinstance(constraints_payload, dict):
        return None

    try:
        return ConstraintSet.model_validate(constraints_payload)
    except Exception:
        return None


@router.post("/recommendations", response_model=RecommendationBundle)
async def create_recommendation(
    request: PlanRequest,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RecommendationBundle:
    ensure_user(db, current_user)
    if request.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden user scope")

    effective_request = build_effective_plan_request(db, request, current_user.user_id)
    rec = await execute_plan_request(db=db, request=effective_request, trigger="create_recommendation")
    return _to_bundle(rec)


@router.post("/recommendations/{recommendation_id}/replan", response_model=RecommendationBundle)
async def replan_recommendation(
    recommendation_id: str,
    payload: ReplanRequest | None = None,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RecommendationBundle:
    original = db.get(Recommendation, recommendation_id)
    if not original:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")
    if original.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden recommendation scope")

    prior_message = f"[Prior recipe: {original.recipe_title}] " + (
        (payload.user_message or "") if payload else ""
    )
    inherited_constraints = _load_constraints_from_recommendation_run(db, recommendation_id) or ConstraintSet()

    base_request = build_effective_plan_request(
        db,
        PlanRequest(
            user_id=current_user.user_id,
            constraints=inherited_constraints,
            user_message=prior_message or None,
        ),
        current_user.user_id,
    )

    constraints = base_request.constraints
    if payload and payload.constraints:
        constraints = merge_constraints(base_request.constraints, payload.constraints)

    effective_request = PlanRequest(
        user_id=current_user.user_id,
        constraints=constraints,
        inventory=base_request.inventory,
        latest_meal_log=base_request.latest_meal_log,
        user_message=prior_message or base_request.user_message,
        prior_recipe_hint=original.recipe_metadata or None,
    )
    replanned = await execute_plan_request(
        db=db,
        request=effective_request,
        trigger=f"manual_replan:{recommendation_id}",
    )
    return _to_bundle(replanned)


@router.get("/recommendations/{recommendation_id}", response_model=RecommendationBundle)
async def get_recommendation(
    recommendation_id: str,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RecommendationBundle:
    rec = db.get(Recommendation, recommendation_id)
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")
    if rec.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden recommendation scope")
    return _to_bundle(rec)


@router.get("/recommendations/history/{user_id}", response_model=list[RecommendationBundle])
async def list_recommendation_history(
    user_id: str,
    limit: int = Query(default=20, ge=1, le=100),
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[RecommendationBundle]:
    if user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden user scope")

    rows = (
        db.execute(
            select(Recommendation)
            .where(Recommendation.user_id == user_id)
            .order_by(Recommendation.created_at.desc())
            .limit(limit)
        )
        .scalars()
        .all()
    )
    return [_to_bundle(rec) for rec in rows]


@router.get("/recommendations/latest/{user_id}", response_model=RecommendationBundle)
async def get_latest_recommendation(
    user_id: str,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RecommendationBundle:
    if user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden user scope")

    latest = db.execute(
        select(Recommendation).where(Recommendation.user_id == user_id).order_by(Recommendation.created_at.desc())
    ).scalars().first()
    if not latest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No recommendation found")
    return _to_bundle(latest)


@router.get("/runs/latest/{user_id}")
async def get_latest_plan_run(
    user_id: str,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    if user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden user scope")

    run = (
        db.execute(select(PlanRun).where(PlanRun.user_id == user_id).order_by(PlanRun.created_at.desc()))
        .scalars()
        .first()
    )
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No plan run found")

    return {
        "run_id": run.id,
        "status": run.status,
        "mode": run.mode,
        "trace_notes": run.trace_notes,
        "recommendation_id": run.recommendation_id,
        "created_at": run.created_at.isoformat() if run.created_at else None,
        "completed_at": run.completed_at.isoformat() if run.completed_at else None,
    }


@router.get("/recommendations/{recommendation_id}/recipe")
async def get_recipe_detail(
    recommendation_id: str,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    rec = db.get(Recommendation, recommendation_id)
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")
    if rec.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden recommendation scope")
    bundle = recommendation_to_bundle(rec)
    return {
        "recommendation_id": rec.id,
        "recipe_title": bundle.decision.recipe_title,
        "steps": bundle.meal_plan.steps,
        "recipe_metadata": rec.recipe_metadata or {},
    }


@router.get("/recommendations/{recommendation_id}/nutrition")
async def get_nutrition_summary(
    recommendation_id: str,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    rec = db.get(Recommendation, recommendation_id)
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")
    if rec.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden recommendation scope")
    bundle = recommendation_to_bundle(rec)
    return bundle.meal_plan.nutrition_summary.model_dump()


@router.get("/recommendations/{recommendation_id}/grocery-gap")
async def get_grocery_gap(
    recommendation_id: str,
    current_user: AuthContext = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[dict]:
    rec = db.get(Recommendation, recommendation_id)
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")
    if rec.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden recommendation scope")
    bundle = recommendation_to_bundle(rec)
    return [item.model_dump() for item in bundle.grocery_plan.missing_ingredients]

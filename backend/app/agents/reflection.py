"""Reflection validators for recommendation safety and constraint compliance."""

from __future__ import annotations

from app.schemas.contracts import PlanRequest, RecommendationBundle


def apply_reflection(bundle: RecommendationBundle, request: PlanRequest) -> tuple[RecommendationBundle, list[str]]:
    """Enforce hard constraints and return reflection notes."""

    notes: list[str] = []

    # Hard guard: remove allergen ingredients from grocery gap if known.
    allergies = {a.lower() for a in request.constraints.allergies}
    if allergies and bundle.grocery_gap:
        filtered = [g for g in bundle.grocery_gap if g.ingredient.lower() not in allergies]
        if len(filtered) != len(bundle.grocery_gap):
            notes.append("Removed allergen ingredients from grocery gap during reflection")
            bundle.grocery_gap = filtered

    calories_target = request.constraints.calories_target
    if calories_target is not None and bundle.nutrition_summary.calories > calories_target:
        notes.append("Calorie target exceeded; adjusted output with lower-calorie guidance")
        bundle.substitutions.append("Use a smaller portion or lower-calorie protein swap")

    if not notes:
        notes.append("Reflection checks passed")

    return bundle, notes

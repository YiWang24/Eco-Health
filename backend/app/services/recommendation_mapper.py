"""Mapping helpers between ORM recommendation rows and canonical API contracts."""

from __future__ import annotations

from functools import lru_cache

from app.models.recommendation import Recommendation
from app.schemas.contracts import (
    DecisionBlock,
    ExecutionPlanBlock,
    GroceryItem,
    GroceryPlanBlock,
    MealPlanBlock,
    MemoryUpdatesBlock,
    NutritionSummary,
    RecommendationBundle,
    ReflectionBlock,
)
from app.services.planner import resolve_recipe_metadata_for_title


_PUBLIC_RECIPE_METADATA_KEYS = {
    "recipe_id",
    "recipe_title",
    "category",
    "area",
    "tags",
    "thumbnail_url",
    "youtube_url",
    "source_url",
    "ingredient_details",
    "api_source",
}


def _public_recipe_metadata(metadata: dict) -> dict:
    if not isinstance(metadata, dict):
        return {}
    return {key: metadata.get(key) for key in _PUBLIC_RECIPE_METADATA_KEYS if key in metadata}


@lru_cache(maxsize=256)
def _resolve_metadata_for_title(recipe_title: str) -> dict:
    return resolve_recipe_metadata_for_title(recipe_title, inventory=None, constraints=None)


def _with_metadata_backfill(metadata: dict, recipe_title: str) -> dict:
    public = _public_recipe_metadata(metadata)
    if public.get("thumbnail_url") and public.get("recipe_id"):
        return public

    if not recipe_title:
        return public

    resolved = _resolve_metadata_for_title(recipe_title)
    if not resolved:
        return public

    merged = {**resolved, **public}
    if not merged.get("thumbnail_url"):
        merged["thumbnail_url"] = resolved.get("thumbnail_url")
    if not merged.get("recipe_id"):
        merged["recipe_id"] = resolved.get("recipe_id")
    if not merged.get("api_source"):
        merged["api_source"] = resolved.get("api_source")
    return _public_recipe_metadata(merged)


def recommendation_to_bundle(rec: Recommendation) -> RecommendationBundle:
    metadata = rec.recipe_metadata or {}
    enriched_metadata = _with_metadata_backfill(metadata, rec.recipe_title)
    bundle_payload = metadata.get("bundle_v1")
    if isinstance(bundle_payload, dict):
        bundle = RecommendationBundle.model_validate(bundle_payload)
        if bundle.recommendation_id != rec.id:
            bundle.recommendation_id = rec.id
        existing_thumbnail = (bundle.recipe_metadata or {}).get("thumbnail_url")
        if not bundle.recipe_metadata or not existing_thumbnail:
            bundle.recipe_metadata = enriched_metadata
        return bundle

    nutrition = NutritionSummary.model_validate(rec.nutrition_summary or {"calories": 0, "protein_g": 0, "carbs_g": 0, "fat_g": 0})
    gap_items = [GroceryItem.model_validate(item) for item in (rec.grocery_gap or [])]

    decision = DecisionBlock(
        recipe_title=rec.recipe_title,
        rationale=metadata.get("decision_rationale"),
        confidence=metadata.get("confidence"),
    )
    meal_plan = MealPlanBlock(
        steps=rec.steps or [],
        nutrition_summary=nutrition,
        substitutions=rec.substitutions or [],
        spoilage_alerts=rec.spoilage_alerts or [],
    )
    grocery_plan = GroceryPlanBlock(
        missing_ingredients=gap_items,
        optimized_grocery_list=gap_items,
        estimated_gap_cost=float(len(gap_items) * 2.0),
    )

    execution_payload = metadata.get("execution_plan") if isinstance(metadata.get("execution_plan"), dict) else {}
    reflection_payload = metadata.get("reflection") if isinstance(metadata.get("reflection"), dict) else {}
    memory_payload = metadata.get("memory_updates") if isinstance(metadata.get("memory_updates"), dict) else {}

    return RecommendationBundle(
        recommendation_id=rec.id,
        decision=decision,
        meal_plan=meal_plan,
        grocery_plan=grocery_plan,
        recipe_metadata=enriched_metadata,
        execution_plan=ExecutionPlanBlock.model_validate(execution_payload or {}),
        reflection=ReflectionBlock.model_validate(
            reflection_payload
            or {"status": "ok", "attempts": 1, "violations": [], "adjustments": []}
        ),
        memory_updates=MemoryUpdatesBlock.model_validate(
            memory_payload
            or {"short_term_updates": [], "long_term_metric_deltas": {}}
        ),
    )

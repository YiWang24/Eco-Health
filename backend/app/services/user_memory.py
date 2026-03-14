"""Long-term memory aggregation updates for planner outputs and feedback."""

from __future__ import annotations

from collections import Counter
from typing import Any

from sqlalchemy.orm import Session

from app.models.user_memory_profile import UserMemoryProfile
from app.schemas.contracts import InventorySnapshot


def _get_or_create_memory(db: Session, user_id: str) -> UserMemoryProfile:
    memory = db.get(UserMemoryProfile, user_id)
    if memory:
        return memory
    memory = UserMemoryProfile(user_id=user_id)
    db.add(memory)
    db.flush()
    return memory


def _update_purchase_patterns(existing: dict[str, Any], ingredients: list[str]) -> dict[str, Any]:
    counters = Counter(ingredient.lower() for ingredient in ingredients if ingredient)
    next_state = dict(existing or {})
    for ingredient, count in counters.items():
        payload = dict(next_state.get(ingredient) or {"count": 0})
        payload["count"] = int(payload.get("count", 0)) + count
        next_state[ingredient] = payload
    return next_state


def update_memory_after_recommendation(
    *,
    db: Session,
    user_id: str,
    recipe_title: str,
    used_inventory: list[str],
    grocery_gap: list[str],
    spoilage_alerts_count: int,
    expiring_items_used: int,
) -> dict[str, Any]:
    """Update long-term memory metrics after recommendation generation."""

    memory = _get_or_create_memory(db, user_id)

    gap_cost = float(len(grocery_gap) * 2.0)
    pantry_value = float(len(used_inventory) * 2.0)
    money_saved_delta = max(0.0, pantry_value - gap_cost)
    memory.cumulative_money_saved = float(memory.cumulative_money_saved or 0.0) + money_saved_delta

    waste = dict(memory.food_waste_reduction_metrics or {})
    waste["expiring_items_used"] = int(waste.get("expiring_items_used", 0)) + int(expiring_items_used)
    waste["spoilage_alert_meals"] = int(waste.get("spoilage_alert_meals", 0)) + int(spoilage_alerts_count > 0)
    memory.food_waste_reduction_metrics = waste

    sustainability = dict(memory.sustainability_impact_metrics or {})
    sustainability_delta_co2 = round(expiring_items_used * 0.45, 3)
    sustainability_delta_waste = round(expiring_items_used * 0.2, 3)
    sustainability["co2e_kg_saved"] = round(float(sustainability.get("co2e_kg_saved", 0.0)) + sustainability_delta_co2, 3)
    sustainability["waste_kg_avoided"] = round(
        float(sustainability.get("waste_kg_avoided", 0.0)) + sustainability_delta_waste,
        3,
    )
    memory.sustainability_impact_metrics = sustainability

    purchase_inputs = grocery_gap + used_inventory
    memory.purchase_patterns = _update_purchase_patterns(memory.purchase_patterns or {}, purchase_inputs)

    favorites = list(memory.favorite_recipes or [])
    if recipe_title and recipe_title not in favorites:
        favorites.append(recipe_title)
    memory.favorite_recipes = favorites[-20:]
    db.add(memory)

    return {
        "cumulative_money_saved_delta": money_saved_delta,
        "food_waste_reduction_delta": {
            "expiring_items_used": expiring_items_used,
            "spoilage_alert_meals": int(spoilage_alerts_count > 0),
        },
        "sustainability_impact_delta": {
            "co2e_kg_saved": sustainability_delta_co2,
            "waste_kg_avoided": sustainability_delta_waste,
        },
    }


def register_feedback_memory_signal(
    *,
    db: Session,
    user_id: str,
    recipe_title: str,
    action: str,
) -> dict[str, Any]:
    """Apply accept/reject signal to favorite recipes and preference memory."""

    memory = _get_or_create_memory(db, user_id)
    favorites = list(memory.favorite_recipes or [])

    delta: dict[str, Any] = {"favorite_recipe_delta": 0}
    if action == "accept":
        if recipe_title and recipe_title not in favorites:
            favorites.append(recipe_title)
            delta["favorite_recipe_delta"] = 1
    elif action == "reject":
        if recipe_title and recipe_title in favorites:
            favorites.remove(recipe_title)
            delta["favorite_recipe_delta"] = -1

    memory.favorite_recipes = favorites[-20:]
    db.add(memory)
    return delta


def infer_used_inventory(inventory: InventorySnapshot | None, recipe_steps: list[str], recipe_title: str) -> list[str]:
    """Best-effort inventory usage inference for memory updates."""

    if not inventory or not inventory.items:
        return []
    haystack = f"{recipe_title} {' '.join(recipe_steps)}".lower()
    used: list[str] = []
    for item in inventory.items:
        ingredient = item.ingredient.lower()
        if ingredient in haystack:
            used.append(ingredient)
    return used


def count_expiring_items_used(inventory: InventorySnapshot | None, used_inventory: list[str]) -> int:
    """Count expiring ingredients that are actually used by the plan."""

    if not inventory or not inventory.items:
        return 0
    used = {item.lower() for item in used_inventory}
    return sum(
        1
        for item in inventory.items
        if item.expires_in_days is not None and item.expires_in_days <= 2 and item.ingredient.lower() in used
    )

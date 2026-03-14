"""Pydantic schemas for ADK workflow input and output."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AdkGroceryItem(BaseModel):
    ingredient: str
    reason: str


class AdkNutritionSummary(BaseModel):
    calories: int
    protein_g: int
    carbs_g: int
    fat_g: int


class AdkRecommendationOutput(BaseModel):
    recipe_title: str
    steps: list[str] = Field(default_factory=list)
    substitutions: list[str] = Field(default_factory=list)
    spoilage_alerts: list[str] = Field(default_factory=list)
    grocery_gap: list[AdkGroceryItem] = Field(default_factory=list)
    nutrition_summary: AdkNutritionSummary
    confidence_note: str | None = None

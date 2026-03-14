"""Goal request/response schemas."""

from pydantic import BaseModel, Field


class GoalUpsert(BaseModel):
    calories_target: int | None = None
    protein_g_target: int | None = None
    carbs_g_target: int | None = None
    fat_g_target: int | None = None
    dietary_restrictions: list[str] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)
    budget_limit: float | None = None
    max_cook_time_minutes: int | None = None


class GoalResponse(GoalUpsert):
    user_id: str

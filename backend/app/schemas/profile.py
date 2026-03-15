"""Profile request/response schemas."""

from pydantic import BaseModel, Field


class ProfileUpsert(BaseModel):
    age: int | None = None
    biological_sex: str | None = None
    height_cm: float | None = None
    weight_kg: float | None = None
    activity_level: str | None = None
    dietary_preferences: list[str] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)
    cook_time_preference_minutes: int | None = None


class ProfileResponse(ProfileUpsert):
    user_id: str

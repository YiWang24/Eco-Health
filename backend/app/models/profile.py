"""Profile model for onboarding and user context."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    user_id: Mapped[str] = mapped_column(String(128), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(Float, nullable=True)
    activity_level: Mapped[str | None] = mapped_column(String(64), nullable=True)
    dietary_preferences: Mapped[list[str]] = mapped_column(JSON, default=list)
    allergies: Mapped[list[str]] = mapped_column(JSON, default=list)
    cook_time_preference_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

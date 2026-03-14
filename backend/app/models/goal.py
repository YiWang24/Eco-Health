"""Goal model for nutrition and planning constraints."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Goal(Base):
    __tablename__ = "goals"

    user_id: Mapped[str] = mapped_column(String(128), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    calories_target: Mapped[int | None] = mapped_column(Integer, nullable=True)
    protein_g_target: Mapped[int | None] = mapped_column(Integer, nullable=True)
    carbs_g_target: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fat_g_target: Mapped[int | None] = mapped_column(Integer, nullable=True)
    dietary_restrictions: Mapped[list[str]] = mapped_column(JSON, default=list)
    allergies: Mapped[list[str]] = mapped_column(JSON, default=list)
    budget_limit: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_cook_time_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

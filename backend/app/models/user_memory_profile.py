"""Long-term memory aggregate for personalization metrics."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserMemoryProfile(Base):
    __tablename__ = "user_memory_profiles"

    user_id: Mapped[str] = mapped_column(
        String(128),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    favorite_recipes: Mapped[list[str]] = mapped_column(JSON, default=list)
    purchase_patterns: Mapped[dict] = mapped_column(JSON, default=dict)
    cumulative_money_saved: Mapped[float] = mapped_column(Float, default=0.0)
    food_waste_reduction_metrics: Mapped[dict] = mapped_column(
        JSON,
        default=lambda: {"expiring_items_used": 0, "spoilage_alert_meals": 0},
    )
    sustainability_impact_metrics: Mapped[dict] = mapped_column(
        JSON,
        default=lambda: {"co2e_kg_saved": 0.0, "waste_kg_avoided": 0.0},
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

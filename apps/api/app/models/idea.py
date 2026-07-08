"""Idea model — the seed of every mission."""

from __future__ import annotations

from sqlalchemy import JSON, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base
from .base import TimestampMixin, UUIDMixin


class Idea(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "ideas"

    organization_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("organizations.id")
    )
    created_by_user_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id")
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    seed_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, nullable=False, default="raw")
    tags: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    idea_score: Mapped[float | None] = mapped_column(Float)
    risk_score: Mapped[float | None] = mapped_column(Float)
    readiness_score: Mapped[float | None] = mapped_column(Float)
    # `metadata` is reserved on the declarative base, so map attr -> column name.
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, nullable=False, default=dict)

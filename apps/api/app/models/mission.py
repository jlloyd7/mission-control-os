"""Missions, mission runs, and run steps (the execution timeline)."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base
from .base import TimestampMixin, UUIDMixin


class Mission(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "missions"

    organization_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("organizations.id")
    )
    source_idea_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("ideas.id"))
    source_blueprint_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("blueprints.id")
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    objective: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="draft")
    priority: Mapped[str] = mapped_column(String, nullable=False, default="normal")
    owner_user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    risk_level: Mapped[str] = mapped_column(String, nullable=False, default="medium")
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, nullable=False, default=dict)


class MissionRun(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "mission_runs"

    mission_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("missions.id"), nullable=False
    )
    organization_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("organizations.id")
    )
    status: Mapped[str] = mapped_column(String, nullable=False, default="queued")
    run_mode: Mapped[str] = mapped_column(String, nullable=False, default="mock")
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    total_input_tokens: Mapped[int] = mapped_column(Integer, default=0)
    total_output_tokens: Mapped[int] = mapped_column(Integer, default=0)
    estimated_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    error_message: Mapped[str | None] = mapped_column(Text)
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, nullable=False, default=dict)


class RunStep(UUIDMixin, Base):
    __tablename__ = "run_steps"

    run_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("mission_runs.id"))
    council_run_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("council_runs.id")
    )
    organization_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("organizations.id")
    )
    step_index: Mapped[int] = mapped_column(Integer, nullable=False)
    step_type: Mapped[str] = mapped_column(String, nullable=False)
    agent_key: Mapped[str | None] = mapped_column(String)
    title: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    input_payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    output_payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String, nullable=False, default="completed")
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

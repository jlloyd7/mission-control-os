"""Council runs, agent contributions, extracted best parts, and blueprints."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base
from .base import TimestampMixin, UUIDMixin


class CouncilRun(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "council_runs"

    idea_id: Mapped[str] = mapped_column(String(36), ForeignKey("ideas.id"), nullable=False)
    organization_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("organizations.id")
    )
    status: Mapped[str] = mapped_column(String, nullable=False, default="queued")
    mode: Mapped[str] = mapped_column(String, nullable=False, default="triad")
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error_message: Mapped[str | None] = mapped_column(Text)
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, nullable=False, default=dict)


class CouncilContribution(UUIDMixin, Base):
    __tablename__ = "council_contributions"

    council_run_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("council_runs.id"), nullable=False
    )
    agent_key: Mapped[str] = mapped_column(String, nullable=False)
    agent_name: Mapped[str] = mapped_column(String, nullable=False)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    model_name: Mapped[str] = mapped_column(String, nullable=False)
    contribution_type: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str | None] = mapped_column(String)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    confidence: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class BestPart(UUIDMixin, Base):
    __tablename__ = "best_parts"

    idea_id: Mapped[str] = mapped_column(String(36), ForeignKey("ideas.id"), nullable=False)
    council_run_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("council_runs.id")
    )
    source_agent_key: Mapped[str] = mapped_column(String, nullable=False)
    part_type: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    user_value: Mapped[int | None] = mapped_column(Integer)
    strategic_value: Mapped[int | None] = mapped_column(Integer)
    originality: Mapped[int | None] = mapped_column(Integer)
    feasibility: Mapped[int | None] = mapped_column(Integer)
    revenue_potential: Mapped[int | None] = mapped_column(Integer)
    risk: Mapped[int | None] = mapped_column(Integer)
    build_effort: Mapped[int | None] = mapped_column(Integer)
    weighted_score: Mapped[float | None] = mapped_column(Float)
    decision: Mapped[str] = mapped_column(String, nullable=False, default="keep")
    rationale: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Blueprint(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "blueprints"

    idea_id: Mapped[str] = mapped_column(String(36), ForeignKey("ideas.id"), nullable=False)
    council_run_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("council_runs.id")
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    product_brief: Mapped[str] = mapped_column(Text, nullable=False)
    user_flow: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    feature_list: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    technical_architecture: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    agent_roles: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    tool_requirements: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    risk_controls: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    sprint_plan: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    lineage: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    readiness_score: Mapped[float | None] = mapped_column(Float)

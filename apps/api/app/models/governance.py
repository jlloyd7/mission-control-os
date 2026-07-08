"""Tools, approvals, artifacts, and audit logs."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base
from .base import TimestampMixin, UUIDMixin


class Tool(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "tools"
    __table_args__ = (UniqueConstraint("organization_id", "key", name="uq_tool_org_key"),)

    organization_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("organizations.id")
    )
    key: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    tool_type: Mapped[str] = mapped_column(String, nullable=False, default="function")
    input_schema: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    output_schema: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    can_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    can_write: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_delete: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    requires_approval: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    risk_level: Mapped[str] = mapped_column(String, nullable=False, default="medium")
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, nullable=False, default=dict)


class Approval(UUIDMixin, Base):
    __tablename__ = "approvals"

    organization_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("organizations.id")
    )
    mission_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("missions.id"))
    run_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("mission_runs.id"))
    tool_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("tools.id"))
    requested_by_agent_key: Mapped[str | None] = mapped_column(String)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    action_payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    risk_level: Mapped[str] = mapped_column(String, nullable=False, default="medium")
    status: Mapped[str] = mapped_column(String, nullable=False, default="pending")
    decided_by_user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    decision_reason: Mapped[str | None] = mapped_column(Text)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Artifact(UUIDMixin, Base):
    __tablename__ = "artifacts"

    organization_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("organizations.id")
    )
    mission_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("missions.id"))
    run_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("mission_runs.id"))
    idea_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("ideas.id"))
    blueprint_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("blueprints.id"))
    artifact_type: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content_text: Mapped[str | None] = mapped_column(Text)
    content_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    file_url: Mapped[str | None] = mapped_column(String)
    created_by_agent_key: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class AuditLog(UUIDMixin, Base):
    __tablename__ = "audit_logs"

    organization_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("organizations.id")
    )
    actor_user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"))
    actor_agent_key: Mapped[str | None] = mapped_column(String)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    entity_type: Mapped[str] = mapped_column(String, nullable=False)
    entity_id: Mapped[str | None] = mapped_column(String(36))
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

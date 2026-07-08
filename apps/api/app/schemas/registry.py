"""Agent, tool, and approval read schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from .common import ORMModel


class AgentRead(BaseModel):
    id: str
    key: str
    name: str
    persona: str
    provider: str
    model_name: str
    autonomy_level: str
    risk_level: str
    is_enabled: bool
    bbom: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm_agent(cls, a: Any) -> "AgentRead":
        meta = a.metadata_ or {}
        return cls(
            id=a.id,
            key=a.key,
            name=a.name,
            persona=a.persona,
            provider=a.provider,
            model_name=a.model_name,
            autonomy_level=a.autonomy_level,
            risk_level=a.risk_level,
            is_enabled=a.is_enabled,
            bbom=meta.get("bbom_summary", {}),
            created_at=a.created_at,
            updated_at=a.updated_at,
        )


class ToolRead(ORMModel):
    id: str
    key: str
    name: str
    description: str
    tool_type: str
    input_schema: dict = Field(default_factory=dict)
    output_schema: dict = Field(default_factory=dict)
    can_read: bool
    can_write: bool
    can_delete: bool
    requires_approval: bool
    risk_level: str
    is_enabled: bool
    created_at: datetime
    updated_at: datetime


class ApprovalRead(ORMModel):
    id: str
    mission_id: str | None = None
    run_id: str | None = None
    tool_id: str | None = None
    requested_by_agent_key: str | None = None
    title: str
    description: str
    action_payload: dict = Field(default_factory=dict)
    risk_level: str
    status: str
    decided_by_user_id: str | None = None
    decision_reason: str | None = None
    decided_at: datetime | None = None
    created_at: datetime


class ApprovalDecision(BaseModel):
    reason: str | None = None


class AuditLogRead(ORMModel):
    id: str
    actor_user_id: str | None = None
    actor_agent_key: str | None = None
    event_type: str
    entity_type: str
    entity_id: str | None = None
    summary: str
    payload: dict = Field(default_factory=dict)
    created_at: datetime

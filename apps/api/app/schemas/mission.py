"""Mission, mission-run, and run-step schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from .common import ORMModel


class MissionCreate(BaseModel):
    title: str = Field(min_length=1)
    objective: str = Field(min_length=1)
    priority: str = "normal"
    source_idea_id: str | None = None
    source_blueprint_id: str | None = None


class MissionRead(ORMModel):
    id: str
    organization_id: str | None = None
    source_idea_id: str | None = None
    source_blueprint_id: str | None = None
    title: str
    objective: str
    status: str
    priority: str
    owner_user_id: str | None = None
    risk_level: str
    created_at: datetime
    updated_at: datetime


class RunStepRead(ORMModel):
    id: str
    run_id: str | None = None
    council_run_id: str | None = None
    step_index: int
    step_type: str
    agent_key: str | None = None
    title: str
    summary: str | None = None
    input_payload: dict = Field(default_factory=dict)
    output_payload: dict = Field(default_factory=dict)
    status: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    created_at: datetime


class MissionRunRead(ORMModel):
    id: str
    mission_id: str
    status: str
    run_mode: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    total_input_tokens: int
    total_output_tokens: int
    estimated_cost_usd: float
    error_message: str | None = None
    created_at: datetime


class MissionRunDetail(MissionRunRead):
    steps: list[RunStepRead] = Field(default_factory=list)


class MissionDetail(MissionRead):
    runs: list[MissionRunRead] = Field(default_factory=list)

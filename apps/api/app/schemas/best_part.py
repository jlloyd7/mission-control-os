"""Best-part decision (synthesis output) and read model."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from .common import ORMModel
from .council import AgentKey, Decision


class BestPartDecision(BaseModel):
    source_agent_key: AgentKey
    part_type: str
    title: str
    summary: str
    decision: Decision
    rationale: str
    weighted_score: float
    merged_into_blueprint_section: str | None = None


class BestPartRead(ORMModel):
    id: str
    idea_id: str
    council_run_id: str | None = None
    source_agent_key: str
    part_type: str
    title: str
    summary: str
    user_value: int | None = None
    strategic_value: int | None = None
    originality: int | None = None
    feasibility: int | None = None
    revenue_potential: int | None = None
    risk: int | None = None
    build_effort: int | None = None
    weighted_score: float | None = None
    decision: str
    rationale: str | None = None
    created_at: datetime

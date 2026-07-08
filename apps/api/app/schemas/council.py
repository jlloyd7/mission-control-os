"""Council proposal schema (agent output) and council-run read models."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from .common import ORMModel

AgentKey = Literal["george", "cipher_fable", "arty_codex"]

PartType = Literal[
    "feature",
    "ux",
    "architecture",
    "automation",
    "security",
    "business",
    "launch",
    "risk",
    "open_source",
]

Decision = Literal["keep", "modify", "reject", "needs_evidence", "needs_human_approval"]


class ScoreBlock(BaseModel):
    user_value: int = Field(ge=1, le=10)
    strategic_value: int = Field(ge=1, le=10)
    originality: int = Field(ge=1, le=10)
    feasibility: int = Field(ge=1, le=10)
    revenue_potential: int = Field(ge=1, le=10)
    risk: int = Field(ge=1, le=10)
    build_effort: int = Field(ge=1, le=10)


class IdeaFragment(BaseModel):
    part_type: PartType
    title: str
    summary: str
    why_it_matters: str
    score: ScoreBlock
    recommended_decision: Decision


class CouncilProposal(BaseModel):
    agent_key: AgentKey
    title: str
    summary: str
    assumptions: list[str] = Field(default_factory=list)
    proposal: str
    best_features: list[IdeaFragment] = Field(default_factory=list)
    weak_points: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    build_steps: list[str] = Field(default_factory=list)
    human_approval_needed: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)


# --- read models ----------------------------------------------------------


class CouncilContributionRead(ORMModel):
    id: str
    council_run_id: str
    agent_key: str
    agent_name: str
    provider: str
    model_name: str
    contribution_type: str
    title: str | None = None
    summary: str
    content: dict = Field(default_factory=dict)
    confidence: float | None = None
    created_at: datetime


class CouncilRunRead(ORMModel):
    id: str
    idea_id: str
    status: str
    mode: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    created_at: datetime


class CouncilRunDetail(CouncilRunRead):
    contributions: list[CouncilContributionRead] = Field(default_factory=list)

"""Blueprint read/update schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from .common import ORMModel


class BlueprintRead(ORMModel):
    id: str
    idea_id: str
    council_run_id: str | None = None
    title: str
    summary: str
    product_brief: str
    user_flow: list = Field(default_factory=list)
    feature_list: list = Field(default_factory=list)
    technical_architecture: dict = Field(default_factory=dict)
    agent_roles: dict = Field(default_factory=dict)
    tool_requirements: list = Field(default_factory=list)
    risk_controls: list = Field(default_factory=list)
    sprint_plan: list = Field(default_factory=list)
    lineage: list = Field(default_factory=list)
    readiness_score: float | None = None
    created_at: datetime
    updated_at: datetime


class BlueprintUpdate(BaseModel):
    title: str | None = None
    summary: str | None = None
    product_brief: str | None = None

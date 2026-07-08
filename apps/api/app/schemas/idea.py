"""Idea request/response schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from .common import ORMModel


class IdeaCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    seed_prompt: str = Field(min_length=1)
    description: str | None = None
    tags: list[str] = Field(default_factory=list)
    target_output_type: str | None = None
    autonomy_preference: str | None = None


class IdeaUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    description: str | None = None
    tags: list[str] | None = None
    status: str | None = None


class IdeaRead(ORMModel):
    id: str
    title: str
    seed_prompt: str
    description: str | None = None
    status: str
    tags: list[str] = Field(default_factory=list)
    idea_score: float | None = None
    risk_score: float | None = None
    readiness_score: float | None = None
    created_at: datetime
    updated_at: datetime

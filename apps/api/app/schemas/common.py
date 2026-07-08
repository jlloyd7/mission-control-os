"""Shared schema helpers."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    """Base for read models sourced from ORM objects."""

    model_config = ConfigDict(from_attributes=True)

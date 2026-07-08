"""Model provider interface — the seam between the orchestrator and any LLM."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field


class ModelMessage(BaseModel):
    role: str
    content: str


class ModelRequest(BaseModel):
    model: str
    system_prompt: str
    messages: list[ModelMessage]
    response_schema: dict[str, Any] | None = None
    temperature: float = 0.2
    max_tokens: int | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ModelUsage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost_usd: float = 0.0


class ModelResponse(BaseModel):
    content_text: str
    content_json: dict[str, Any] | None = None
    usage: ModelUsage = Field(default_factory=ModelUsage)
    raw: dict[str, Any] = Field(default_factory=dict)


class ModelProvider(ABC):
    """All providers (mock, OpenAI, Anthropic) implement this one method."""

    name: str = "base"

    @abstractmethod
    async def complete(self, request: ModelRequest) -> ModelResponse:
        raise NotImplementedError

"""Anthropic provider adapter — P1/P7 stub.

Kept behind ENABLE_REAL_MODELS. Implement with the Anthropic Messages API or the
Claude Agent SDK. Keep tool execution disabled until the tool gateway + approvals
are ready.
"""

from __future__ import annotations

from .base import ModelProvider, ModelRequest, ModelResponse


class AnthropicProvider(ModelProvider):
    name = "anthropic"

    async def complete(self, request: ModelRequest) -> ModelResponse:  # noqa: ARG002
        # TODO(P7): call Anthropic, validate structured output, map usage/cost.
        raise NotImplementedError(
            "AnthropicProvider is not implemented yet. Set ENABLE_REAL_MODELS=false "
            "to use the mock provider."
        )

"""OpenAI provider adapter — P1/P7 stub.

Kept behind ENABLE_REAL_MODELS. Implement with the OpenAI Responses/Agents SDK
and parse structured JSON into the CouncilProposal schema.
"""

from __future__ import annotations

from .base import ModelProvider, ModelRequest, ModelResponse


class OpenAIProvider(ModelProvider):
    name = "openai"

    async def complete(self, request: ModelRequest) -> ModelResponse:  # noqa: ARG002
        # TODO(P7): call OpenAI, validate structured output, map usage/cost.
        raise NotImplementedError(
            "OpenAIProvider is not implemented yet. Set ENABLE_REAL_MODELS=false "
            "to use the mock provider."
        )

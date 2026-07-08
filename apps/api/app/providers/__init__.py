"""Provider registry. Mock by default; real providers behind ENABLE_REAL_MODELS."""

from __future__ import annotations

from ..config import get_settings
from .base import (
    ModelMessage,
    ModelProvider,
    ModelRequest,
    ModelResponse,
    ModelUsage,
)
from .mock_provider import MockProvider

__all__ = [
    "ModelMessage",
    "ModelProvider",
    "ModelRequest",
    "ModelResponse",
    "ModelUsage",
    "MockProvider",
    "get_provider",
]


def get_provider(provider_name: str | None = None) -> ModelProvider:
    """Resolve a provider by name, honoring the ENABLE_REAL_MODELS flag.

    In P0 (default) this always returns the mock provider so the flow runs with
    no API keys.  # TODO(P7): wire real OpenAI/Anthropic adapters.
    """
    settings = get_settings()
    name = (provider_name or settings.default_model_provider or "mock").lower()

    if not settings.enable_real_models:
        return MockProvider()

    if name == "openai":
        from .openai_provider import OpenAIProvider

        return OpenAIProvider()
    if name == "anthropic":
        from .anthropic_provider import AnthropicProvider

        return AnthropicProvider()
    return MockProvider()

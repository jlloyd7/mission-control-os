"""Anthropic provider adapter (P1). Only reachable when ENABLE_REAL_MODELS=true.

Tool execution stays disabled; this only produces structured council proposals.
"""

from __future__ import annotations

import json
from typing import Any

from ..config import get_settings
from .base import ModelProvider, ModelRequest, ModelResponse, ModelUsage


def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text[:4].lower() == "json":
            text = text[4:]
        text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end > start:
            return json.loads(text[start : end + 1])
        raise


class AnthropicProvider(ModelProvider):
    name = "anthropic"

    async def complete(self, request: ModelRequest) -> ModelResponse:
        settings = get_settings()
        if not settings.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set; cannot use the Anthropic provider.")
        try:
            from anthropic import AsyncAnthropic
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "anthropic package not installed. Run: uv pip install -e \".[real]\""
            ) from exc

        client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        system = (
            request.system_prompt
            + "\n\nRespond with ONLY a single JSON object — no prose, no code fences."
        )
        if request.response_schema:
            system += "\nJSON schema:\n" + json.dumps(request.response_schema)

        resp = await client.messages.create(
            model=request.model,
            system=system,
            max_tokens=request.max_tokens or 4096,
            temperature=request.temperature,
            messages=[{"role": m.role, "content": m.content} for m in request.messages],
        )
        text = "".join(
            block.text for block in resp.content if getattr(block, "type", "") == "text"
        ) or "{}"
        return ModelResponse(
            content_text=text,
            content_json=_extract_json(text),
            usage=ModelUsage(
                input_tokens=getattr(resp.usage, "input_tokens", 0) or 0,
                output_tokens=getattr(resp.usage, "output_tokens", 0) or 0,
            ),
            raw={"provider": "anthropic", "model": request.model},
        )

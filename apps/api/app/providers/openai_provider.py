"""OpenAI provider adapter (P1). Only reachable when ENABLE_REAL_MODELS=true."""

from __future__ import annotations

import json
from typing import Any

from ..config import get_settings
from .base import ModelProvider, ModelRequest, ModelResponse, ModelUsage


def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end > start:
            return json.loads(text[start : end + 1])
        raise


class OpenAIProvider(ModelProvider):
    name = "openai"

    async def complete(self, request: ModelRequest) -> ModelResponse:
        settings = get_settings()
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not set; cannot use the OpenAI provider.")
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "openai package not installed. Run: uv pip install -e \".[real]\""
            ) from exc

        client = AsyncOpenAI(api_key=settings.openai_api_key)
        system = request.system_prompt
        if request.response_schema:
            system += "\n\nReturn ONLY JSON matching this schema:\n" + json.dumps(
                request.response_schema
            )
        messages = [{"role": "system", "content": system}] + [
            {"role": m.role, "content": m.content} for m in request.messages
        ]

        resp = await client.chat.completions.create(
            model=request.model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            response_format={"type": "json_object"},
        )
        text = resp.choices[0].message.content or "{}"
        usage = resp.usage
        return ModelResponse(
            content_text=text,
            content_json=_extract_json(text),
            usage=ModelUsage(
                input_tokens=getattr(usage, "prompt_tokens", 0) or 0,
                output_tokens=getattr(usage, "completion_tokens", 0) or 0,
            ),
            raw={"provider": "openai", "model": request.model},
        )

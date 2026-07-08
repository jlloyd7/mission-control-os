"""Health and version endpoints."""

from __future__ import annotations

from fastapi import APIRouter

from ..config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/version")
def version() -> dict:
    s = get_settings()
    return {
        "name": s.app_name,
        "version": "0.1.0",
        "env": s.app_env,
        "real_models": s.enable_real_models,
        "provider": s.default_model_provider,
    }

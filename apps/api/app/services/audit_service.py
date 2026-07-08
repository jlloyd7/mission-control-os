"""Audit log and run-step helpers — the internal trace surface (P0 observability)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .. import models


def log_event(
    db: Session,
    *,
    org_id: str | None,
    event_type: str,
    entity_type: str,
    entity_id: str | None,
    summary: str,
    payload: dict[str, Any] | None = None,
    actor_user_id: str | None = None,
    actor_agent_key: str | None = None,
) -> models.AuditLog:
    entry = models.AuditLog(
        organization_id=org_id,
        actor_user_id=actor_user_id,
        actor_agent_key=actor_agent_key,
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        summary=summary,
        payload=payload or {},
    )
    db.add(entry)
    return entry


def next_step_index(db: Session, *, council_run_id: str | None = None, run_id: str | None = None) -> int:
    stmt = select(func.count()).select_from(models.RunStep)
    if council_run_id is not None:
        stmt = stmt.where(models.RunStep.council_run_id == council_run_id)
    if run_id is not None:
        stmt = stmt.where(models.RunStep.run_id == run_id)
    return int(db.scalar(stmt) or 0)


def add_run_step(
    db: Session,
    *,
    step_type: str,
    title: str,
    org_id: str | None = None,
    council_run_id: str | None = None,
    run_id: str | None = None,
    step_index: int | None = None,
    agent_key: str | None = None,
    summary: str | None = None,
    input_payload: dict[str, Any] | None = None,
    output_payload: dict[str, Any] | None = None,
    status: str = "completed",
    error_message: str | None = None,
) -> models.RunStep:
    if step_index is None:
        step_index = next_step_index(db, council_run_id=council_run_id, run_id=run_id)
    step = models.RunStep(
        organization_id=org_id,
        council_run_id=council_run_id,
        run_id=run_id,
        step_index=step_index,
        step_type=step_type,
        agent_key=agent_key,
        title=title,
        summary=summary,
        input_payload=input_payload or {},
        output_payload=output_payload or {},
        status=status,
        error_message=error_message,
        completed_at=datetime.now(timezone.utc) if status == "completed" else None,
    )
    db.add(step)
    return step

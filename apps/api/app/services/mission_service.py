"""Promote blueprints into missions and run them (mock timeline)."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from .. import models
from ..enums import IdeaStatus
from . import audit_service


def _now() -> datetime:
    return datetime.now(timezone.utc)


def promote_to_mission(
    db: Session, *, idea: models.Idea, org_id: str, user_id: str
) -> models.Mission:
    blueprint = db.scalar(
        select(models.Blueprint)
        .filter_by(idea_id=idea.id)
        .order_by(desc(models.Blueprint.created_at))
    )
    if blueprint is None:
        raise ValueError("No blueprint found. Generate a blueprint first.")

    # Idempotency (P1.4): never create a silent duplicate mission for an idea.
    existing = db.scalar(
        select(models.Mission).where(
            models.Mission.source_idea_id == idea.id,
            models.Mission.status != "cancelled",
        )
    )
    if existing is not None:
        raise ValueError(
            "This idea is already promoted to a mission. "
            "Cancel the existing mission before re-promoting."
        )

    mission = models.Mission(
        organization_id=org_id,
        source_idea_id=idea.id,
        source_blueprint_id=blueprint.id,
        title=idea.title,
        objective=blueprint.summary or idea.seed_prompt,
        status="draft",
        priority="normal",
        owner_user_id=user_id,
        risk_level="medium",
    )
    db.add(mission)
    db.flush()

    # Initial run captures the creation lineage so the timeline shows events.
    run = models.MissionRun(
        mission_id=mission.id,
        organization_id=org_id,
        status="completed",
        run_mode="mock",
        started_at=_now(),
        completed_at=_now(),
    )
    db.add(run)
    db.flush()

    creation_steps = [
        ("user_input", "Mission created from blueprint", idea.title),
        ("artifact_created", "Blueprint linked", blueprint.title),
        ("agent_thought_summary", "Ready for run",
         "Mission is in draft; start a run to execute (mock mode)."),
    ]
    for i, (step_type, title, summary) in enumerate(creation_steps):
        audit_service.add_run_step(
            db, run_id=run.id, org_id=org_id, step_index=i,
            step_type=step_type, title=title, summary=summary,
        )

    idea.status = IdeaStatus.promoted_to_mission.value
    audit_service.log_event(
        db,
        org_id=org_id,
        actor_user_id=user_id,
        event_type="mission.created_from_blueprint",
        entity_type="mission",
        entity_id=mission.id,
        summary=f"Mission created from blueprint {blueprint.title!r}",
    )
    db.commit()
    db.refresh(mission)
    return mission


def start_run(db: Session, *, mission: models.Mission, org_id: str) -> models.MissionRun:
    run = models.MissionRun(
        mission_id=mission.id,
        organization_id=org_id,
        status="running",
        run_mode="mock",
        started_at=_now(),
    )
    db.add(run)
    db.flush()

    steps = [
        ("user_input", "Run started", "Executing mission in mock mode.", None),
        ("agent_proposal", "George plans execution", "Break the objective into staged steps.", "george"),
        ("tool_call", "knowledge_search (mock)", "Simulated read-only knowledge lookup.", "george"),
        ("tool_result", "knowledge_search result", "Returned mock context for planning.", None),
        ("artifact_created", "Draft output", "Mock artifact produced for review.", "arty_codex"),
    ]
    for i, (step_type, title, summary, agent_key) in enumerate(steps):
        audit_service.add_run_step(
            db, run_id=run.id, org_id=org_id, step_index=i,
            step_type=step_type, title=title, summary=summary, agent_key=agent_key,
        )

    run.status = "completed"
    run.completed_at = _now()
    run.total_input_tokens = 320
    run.total_output_tokens = 210
    run.estimated_cost_usd = 0.0
    mission.status = "completed"

    audit_service.log_event(
        db,
        org_id=org_id,
        event_type="mission.run_completed",
        entity_type="mission_run",
        entity_id=run.id,
        summary=f"Mock run completed for mission {mission.title!r}",
    )
    db.commit()
    db.refresh(run)
    return run

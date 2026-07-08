"""Runs the three-seat council (mock by default) and records contributions + steps."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models
from ..enums import IdeaStatus
from ..providers import ModelMessage, ModelRequest, get_provider
from ..schemas.council import CouncilProposal
from . import audit_service

COUNCIL_ORDER = ["george", "cipher_fable", "arty_codex"]


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _idea_prompt(idea: models.Idea) -> str:
    tags = ", ".join(idea.tags or [])
    parts = [f"Idea title: {idea.title}", f"Seed prompt: {idea.seed_prompt}"]
    if idea.description:
        parts.append(f"Description: {idea.description}")
    if tags:
        parts.append(f"Tags: {tags}")
    parts.append("Return a CouncilProposal for your seat.")
    return "\n".join(parts)


async def run_council(db: Session, *, idea: models.Idea, org_id: str) -> models.CouncilRun:
    run = models.CouncilRun(
        idea_id=idea.id,
        organization_id=org_id,
        status="running",
        mode="triad",
        started_at=_now(),
    )
    db.add(run)
    db.flush()

    audit_service.add_run_step(
        db,
        council_run_id=run.id,
        org_id=org_id,
        step_type="user_input",
        title="Council started",
        summary=idea.seed_prompt[:280],
    )
    idea.status = IdeaStatus.council_running.value

    for key in COUNCIL_ORDER:
        agent = db.scalar(select(models.Agent).filter_by(organization_id=org_id, key=key))
        if agent is None or not agent.is_enabled:
            continue
        version = db.scalar(select(models.AgentVersion).filter_by(agent_id=agent.id, version=1))
        system_prompt = version.system_prompt if version else ""

        request = ModelRequest(
            model=agent.model_name,
            system_prompt=system_prompt,
            messages=[ModelMessage(role="user", content=_idea_prompt(idea))],
            metadata={"agent_key": key},
        )
        try:
            provider = get_provider(agent.provider)
            resp = await provider.complete(request)
            proposal = CouncilProposal.model_validate(resp.content_json)
            db.add(models.CouncilContribution(
                council_run_id=run.id,
                agent_key=key,
                agent_name=agent.name,
                provider=agent.provider,
                model_name=agent.model_name,
                contribution_type="proposal",
                title=proposal.title,
                summary=proposal.summary,
                content=proposal.model_dump(),
                confidence=proposal.confidence,
            ))
            audit_service.add_run_step(
                db,
                council_run_id=run.id,
                org_id=org_id,
                step_type="agent_proposal",
                agent_key=key,
                title=f"{agent.name}: {proposal.title}",
                summary=proposal.summary,
                output_payload={
                    "usage": resp.usage.model_dump(),
                    "confidence": proposal.confidence,
                    "best_features": len(proposal.best_features),
                    "risks": len(proposal.risks),
                },
            )
        except Exception as exc:  # noqa: BLE001 — never lose prior contributions
            audit_service.add_run_step(
                db,
                council_run_id=run.id,
                org_id=org_id,
                step_type="error",
                agent_key=key,
                title=f"{agent.name} failed",
                summary=str(exc),
                status="failed",
                error_message=str(exc),
            )

    run.status = "completed"
    run.completed_at = _now()
    idea.status = IdeaStatus.council_complete.value
    audit_service.log_event(
        db,
        org_id=org_id,
        event_type="council.completed",
        entity_type="council_run",
        entity_id=run.id,
        summary=f"Council completed for idea {idea.title!r}",
    )
    db.commit()
    db.refresh(run)
    return run

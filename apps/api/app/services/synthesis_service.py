"""Best-parts extraction and blueprint synthesis (deterministic in mock mode)."""

from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from .. import models
from ..enums import IdeaStatus
from ..schemas.council import CouncilProposal
from . import audit_service, scoring_service

_KEEP = ("keep", "modify")


def _latest_council_run(db: Session, idea_id: str) -> models.CouncilRun | None:
    return db.scalar(
        select(models.CouncilRun)
        .filter_by(idea_id=idea_id)
        .order_by(desc(models.CouncilRun.created_at))
    )


def extract_best_parts(db: Session, *, idea: models.Idea, org_id: str) -> list[models.BestPart]:
    run = _latest_council_run(db, idea.id)
    if run is None:
        raise ValueError("No council run found. Run the council first.")

    contributions = db.scalars(
        select(models.CouncilContribution).filter_by(council_run_id=run.id)
    ).all()

    # Idempotent: clear prior extraction for this idea.
    for old in db.scalars(select(models.BestPart).filter_by(idea_id=idea.id)).all():
        db.delete(old)
    db.flush()

    parts: list[models.BestPart] = []
    for contribution in contributions:
        try:
            proposal = CouncilProposal.model_validate(contribution.content)
        except Exception:  # noqa: BLE001 — skip malformed contribution
            continue
        for frag in proposal.best_features:
            s = frag.score
            weighted = scoring_service.weighted_part_score(
                s.user_value, s.strategic_value, s.originality,
                s.feasibility, s.revenue_potential, s.risk, s.build_effort,
            )
            part = models.BestPart(
                idea_id=idea.id,
                council_run_id=run.id,
                source_agent_key=proposal.agent_key,
                part_type=frag.part_type,
                title=frag.title,
                summary=frag.summary,
                user_value=s.user_value,
                strategic_value=s.strategic_value,
                originality=s.originality,
                feasibility=s.feasibility,
                revenue_potential=s.revenue_potential,
                risk=s.risk,
                build_effort=s.build_effort,
                weighted_score=weighted,
                decision=frag.recommended_decision,
                rationale=frag.why_it_matters,
            )
            db.add(part)
            parts.append(part)

    db.flush()
    idea.status = IdeaStatus.best_parts_extracted.value
    idea.idea_score = scoring_service.idea_score_from_parts(parts)
    idea.risk_score = scoring_service.risk_score_from_parts(parts)

    audit_service.add_run_step(
        db,
        council_run_id=run.id,
        org_id=org_id,
        step_type="best_parts_extraction",
        title="Best parts extracted",
        summary=f"{len(parts)} fragments scored and bucketed by decision",
        output_payload={"count": len(parts)},
    )
    audit_service.log_event(
        db,
        org_id=org_id,
        event_type="best_parts.extracted",
        entity_type="idea",
        entity_id=idea.id,
        summary=f"Extracted {len(parts)} best parts for {idea.title!r}",
    )
    db.commit()
    return parts


def _priority_for(score: float | None) -> str:
    if score is None:
        return "P2"
    if score >= 15:
        return "P0"
    if score >= 8:
        return "P1"
    return "P2"


def generate_blueprint(db: Session, *, idea: models.Idea, org_id: str) -> models.Blueprint:
    run = _latest_council_run(db, idea.id)
    parts = db.scalars(select(models.BestPart).filter_by(idea_id=idea.id)).all()
    if not parts:
        raise ValueError("No best parts found. Extract best parts first.")

    kept = [p for p in parts if p.decision in _KEEP]

    feature_list = [
        {
            "name": p.title,
            "description": p.summary,
            "priority": _priority_for(p.weighted_score),
            "source_agent_keys": [p.source_agent_key],
            "acceptance_criteria": [f"Delivers: {p.title}"],
        }
        for p in kept
    ]
    risk_controls = [p.summary for p in kept if p.part_type in ("security", "risk")] or [
        "Mock/read-only tool defaults",
        "Human approval gates before side effects",
        "Audit logging on every state change",
    ]
    lineage = [
        {"part": p.title, "source_agent": p.source_agent_key, "decision": p.decision}
        for p in kept
    ]

    # Idempotent: replace prior blueprint(s).
    for old in db.scalars(select(models.Blueprint).filter_by(idea_id=idea.id)).all():
        db.delete(old)
    db.flush()

    bp = models.Blueprint(
        idea_id=idea.id,
        council_run_id=run.id if run else None,
        title=f"Blueprint — {idea.title}",
        summary=f"Build-ready blueprint synthesized from {len(kept)} kept fragments.",
        product_brief=idea.seed_prompt,
        user_flow=[
            "Create idea",
            "Run council",
            "Extract best parts",
            "Generate blueprint",
            "Promote to mission",
            "View mission timeline",
        ],
        feature_list=feature_list,
        technical_architecture={
            "frontend": "Next.js App Router + Tailwind",
            "backend": "FastAPI + SQLAlchemy 2",
            "database": "SQLite (dev) / Postgres (prod)",
            "providers": ["mock", "openai", "anthropic"],
        },
        agent_roles={
            "george": "Commander / synthesis",
            "cipher_fable": "Sentinel / risk",
            "arty_codex": "Maker / UX",
        },
        tool_requirements=["knowledge_search", "blueprint_writer", "code_scaffold"],
        risk_controls=risk_controls,
        sprint_plan=[
            {"sprint": 1, "goal": "Vertical slice", "items": ["Idea capture", "Council", "Best parts"]},
            {"sprint": 2, "goal": "Blueprint + mission", "items": ["Blueprint", "Promote", "Timeline"]},
        ],
        lineage=lineage,
    )
    db.add(bp)
    db.flush()
    bp.readiness_score = scoring_service.readiness_score_from_blueprint(bp)

    db.add(models.Artifact(
        organization_id=org_id,
        idea_id=idea.id,
        blueprint_id=bp.id,
        artifact_type="blueprint",
        title=bp.title,
        content_json={"feature_count": len(feature_list), "readiness": bp.readiness_score},
        created_by_agent_key="george",
    ))

    idea.status = IdeaStatus.blueprint_ready.value
    idea.readiness_score = bp.readiness_score

    audit_service.add_run_step(
        db,
        council_run_id=run.id if run else None,
        org_id=org_id,
        step_type="blueprint_generation",
        title="Blueprint generated",
        summary=bp.summary,
        output_payload={"features": len(feature_list), "readiness": bp.readiness_score},
    )
    audit_service.log_event(
        db,
        org_id=org_id,
        event_type="blueprint.generated",
        entity_type="blueprint",
        entity_id=bp.id,
        summary=f"Blueprint generated for {idea.title!r}",
    )
    db.commit()
    db.refresh(bp)
    return bp

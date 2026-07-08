"""Ideas Forge routes — CRUD plus the council → blueprint → mission actions."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select

from .. import models
from ..dependencies import RequestContext, get_context
from ..enums import IdeaStatus
from ..schemas.best_part import BestPartRead
from ..schemas.blueprint import BlueprintRead
from ..schemas.council import CouncilContributionRead, CouncilRunDetail
from ..schemas.idea import IdeaCreate, IdeaRead, IdeaUpdate
from ..schemas.mission import MissionRead
from ..services import audit_service, council_service, mission_service, synthesis_service

router = APIRouter(prefix="/ideas", tags=["ideas"])


def _get_idea(ctx: RequestContext, idea_id: str) -> models.Idea:
    idea = ctx.db.get(models.Idea, idea_id)
    if idea is None or idea.organization_id != ctx.org_id:
        raise HTTPException(status_code=404, detail="Idea not found")
    return idea


def _council_detail(run: models.CouncilRun, contributions) -> CouncilRunDetail:
    detail = CouncilRunDetail.model_validate(run)
    detail.contributions = [CouncilContributionRead.model_validate(c) for c in contributions]
    return detail


@router.get("", response_model=list[IdeaRead])
def list_ideas(ctx: RequestContext = Depends(get_context)):
    return ctx.db.scalars(
        select(models.Idea)
        .where(models.Idea.organization_id == ctx.org_id)
        .order_by(desc(models.Idea.updated_at))
    ).all()


@router.post("", response_model=IdeaRead, status_code=201)
def create_idea(body: IdeaCreate, ctx: RequestContext = Depends(get_context)):
    meta: dict = {}
    if body.target_output_type:
        meta["target_output_type"] = body.target_output_type
    if body.autonomy_preference:
        meta["autonomy_preference"] = body.autonomy_preference

    idea = models.Idea(
        organization_id=ctx.org_id,
        created_by_user_id=ctx.user_id,
        title=body.title,
        seed_prompt=body.seed_prompt,
        description=body.description,
        tags=body.tags,
        status=IdeaStatus.raw.value,
        metadata_=meta,
    )
    ctx.db.add(idea)
    ctx.db.flush()
    audit_service.log_event(
        ctx.db, org_id=ctx.org_id, actor_user_id=ctx.user_id,
        event_type="idea.created", entity_type="idea", entity_id=idea.id,
        summary=f"Idea created: {idea.title!r}",
    )
    ctx.db.commit()
    ctx.db.refresh(idea)
    return idea


@router.get("/{idea_id}", response_model=IdeaRead)
def get_idea(idea_id: str, ctx: RequestContext = Depends(get_context)):
    return _get_idea(ctx, idea_id)


@router.patch("/{idea_id}", response_model=IdeaRead)
def update_idea(idea_id: str, body: IdeaUpdate, ctx: RequestContext = Depends(get_context)):
    idea = _get_idea(ctx, idea_id)
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(idea, key, value)
    ctx.db.commit()
    ctx.db.refresh(idea)
    return idea


@router.delete("/{idea_id}", status_code=204)
def archive_idea(idea_id: str, ctx: RequestContext = Depends(get_context)):
    idea = _get_idea(ctx, idea_id)
    idea.status = IdeaStatus.archived.value
    audit_service.log_event(
        ctx.db, org_id=ctx.org_id, actor_user_id=ctx.user_id,
        event_type="idea.archived", entity_type="idea", entity_id=idea.id,
        summary=f"Idea archived: {idea.title!r}",
    )
    ctx.db.commit()


# --- actions --------------------------------------------------------------


@router.post("/{idea_id}/run-council", response_model=CouncilRunDetail)
async def run_council(idea_id: str, ctx: RequestContext = Depends(get_context)):
    idea = _get_idea(ctx, idea_id)
    run = await council_service.run_council(ctx.db, idea=idea, org_id=ctx.org_id)
    contributions = ctx.db.scalars(
        select(models.CouncilContribution).filter_by(council_run_id=run.id)
    ).all()
    return _council_detail(run, contributions)


@router.post("/{idea_id}/extract-best-parts", response_model=list[BestPartRead])
def extract_best_parts(idea_id: str, ctx: RequestContext = Depends(get_context)):
    idea = _get_idea(ctx, idea_id)
    try:
        return synthesis_service.extract_best_parts(ctx.db, idea=idea, org_id=ctx.org_id)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/{idea_id}/generate-blueprint", response_model=BlueprintRead)
def generate_blueprint(idea_id: str, ctx: RequestContext = Depends(get_context)):
    idea = _get_idea(ctx, idea_id)
    try:
        return synthesis_service.generate_blueprint(ctx.db, idea=idea, org_id=ctx.org_id)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/{idea_id}/promote-to-mission", response_model=MissionRead)
def promote_to_mission(idea_id: str, ctx: RequestContext = Depends(get_context)):
    idea = _get_idea(ctx, idea_id)
    try:
        return mission_service.promote_to_mission(
            ctx.db, idea=idea, org_id=ctx.org_id, user_id=ctx.user_id
        )
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


# --- convenience reads for the idea detail page ---------------------------


@router.get("/{idea_id}/council", response_model=CouncilRunDetail | None)
def latest_council(idea_id: str, ctx: RequestContext = Depends(get_context)):
    _get_idea(ctx, idea_id)
    run = ctx.db.scalar(
        select(models.CouncilRun)
        .filter_by(idea_id=idea_id)
        .order_by(desc(models.CouncilRun.created_at))
    )
    if run is None:
        return None
    contributions = ctx.db.scalars(
        select(models.CouncilContribution).filter_by(council_run_id=run.id)
    ).all()
    return _council_detail(run, contributions)


@router.get("/{idea_id}/best-parts", response_model=list[BestPartRead])
def list_best_parts(idea_id: str, ctx: RequestContext = Depends(get_context)):
    _get_idea(ctx, idea_id)
    return ctx.db.scalars(
        select(models.BestPart)
        .filter_by(idea_id=idea_id)
        .order_by(desc(models.BestPart.weighted_score))
    ).all()


@router.get("/{idea_id}/blueprint", response_model=BlueprintRead | None)
def latest_blueprint(idea_id: str, ctx: RequestContext = Depends(get_context)):
    _get_idea(ctx, idea_id)
    return ctx.db.scalar(
        select(models.Blueprint)
        .filter_by(idea_id=idea_id)
        .order_by(desc(models.Blueprint.created_at))
    )

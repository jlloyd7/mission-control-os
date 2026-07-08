"""Council-run read routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from .. import models
from ..dependencies import RequestContext, get_context
from ..schemas.council import CouncilContributionRead, CouncilRunDetail
from ..schemas.mission import RunStepRead

router = APIRouter(prefix="/council-runs", tags=["council"])


def _get_run(ctx: RequestContext, run_id: str) -> models.CouncilRun:
    run = ctx.db.get(models.CouncilRun, run_id)
    if run is None or run.organization_id != ctx.org_id:
        raise HTTPException(status_code=404, detail="Council run not found")
    return run


@router.get("/{run_id}", response_model=CouncilRunDetail)
def get_council_run(run_id: str, ctx: RequestContext = Depends(get_context)):
    run = _get_run(ctx, run_id)
    contributions = ctx.db.scalars(
        select(models.CouncilContribution).filter_by(council_run_id=run.id)
    ).all()
    detail = CouncilRunDetail.model_validate(run)
    detail.contributions = [CouncilContributionRead.model_validate(c) for c in contributions]
    return detail


@router.get("/{run_id}/contributions", response_model=list[CouncilContributionRead])
def get_contributions(run_id: str, ctx: RequestContext = Depends(get_context)):
    _get_run(ctx, run_id)
    return ctx.db.scalars(
        select(models.CouncilContribution).filter_by(council_run_id=run_id)
    ).all()


@router.get("/{run_id}/steps", response_model=list[RunStepRead])
def get_steps(run_id: str, ctx: RequestContext = Depends(get_context)):
    _get_run(ctx, run_id)
    return ctx.db.scalars(
        select(models.RunStep)
        .filter_by(council_run_id=run_id)
        .order_by(models.RunStep.step_index)
    ).all()

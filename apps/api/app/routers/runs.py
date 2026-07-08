"""Mission-run detail and step routes (the run timeline)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from .. import models
from ..dependencies import RequestContext, get_context
from ..schemas.mission import MissionRunDetail, RunStepRead

router = APIRouter(prefix="/runs", tags=["runs"])


def _get_run(ctx: RequestContext, run_id: str) -> models.MissionRun:
    run = ctx.db.get(models.MissionRun, run_id)
    if run is None or run.organization_id != ctx.org_id:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.get("/{run_id}", response_model=MissionRunDetail)
def get_run(run_id: str, ctx: RequestContext = Depends(get_context)):
    run = _get_run(ctx, run_id)
    steps = ctx.db.scalars(
        select(models.RunStep).filter_by(run_id=run.id).order_by(models.RunStep.step_index)
    ).all()
    detail = MissionRunDetail.model_validate(run)
    detail.steps = [RunStepRead.model_validate(s) for s in steps]
    return detail


@router.get("/{run_id}/steps", response_model=list[RunStepRead])
def get_run_steps(run_id: str, ctx: RequestContext = Depends(get_context)):
    _get_run(ctx, run_id)
    return ctx.db.scalars(
        select(models.RunStep).filter_by(run_id=run_id).order_by(models.RunStep.step_index)
    ).all()

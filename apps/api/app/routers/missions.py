"""Mission board and mission detail routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select

from .. import models
from ..dependencies import RequestContext, get_context
from ..schemas.mission import (
    MissionDetail,
    MissionRead,
    MissionRunRead,
)
from ..services import audit_service, mission_service

router = APIRouter(prefix="/missions", tags=["missions"])


def _get_mission(ctx: RequestContext, mission_id: str) -> models.Mission:
    mission = ctx.db.get(models.Mission, mission_id)
    if mission is None or mission.organization_id != ctx.org_id:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


@router.get("", response_model=list[MissionRead])
def list_missions(ctx: RequestContext = Depends(get_context)):
    return ctx.db.scalars(
        select(models.Mission)
        .where(models.Mission.organization_id == ctx.org_id)
        .order_by(desc(models.Mission.updated_at))
    ).all()


@router.get("/{mission_id}", response_model=MissionDetail)
def get_mission(mission_id: str, ctx: RequestContext = Depends(get_context)):
    mission = _get_mission(ctx, mission_id)
    runs = ctx.db.scalars(
        select(models.MissionRun)
        .filter_by(mission_id=mission.id)
        .order_by(desc(models.MissionRun.created_at))
    ).all()
    detail = MissionDetail.model_validate(mission)
    detail.runs = [MissionRunRead.model_validate(r) for r in runs]
    return detail


@router.post("/{mission_id}/start-run", response_model=MissionRunRead)
def start_run(mission_id: str, ctx: RequestContext = Depends(get_context)):
    mission = _get_mission(ctx, mission_id)
    return mission_service.start_run(ctx.db, mission=mission, org_id=ctx.org_id)


@router.post("/{mission_id}/cancel", response_model=MissionRead)
def cancel_mission(mission_id: str, ctx: RequestContext = Depends(get_context)):
    mission = _get_mission(ctx, mission_id)
    mission.status = "cancelled"
    audit_service.log_event(
        ctx.db, org_id=ctx.org_id, actor_user_id=ctx.user_id,
        event_type="mission.cancelled", entity_type="mission", entity_id=mission.id,
        summary=f"Mission cancelled: {mission.title!r}",
    )
    ctx.db.commit()
    ctx.db.refresh(mission)
    return mission

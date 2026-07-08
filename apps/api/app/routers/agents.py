"""Agent registry routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select

from .. import models
from ..dependencies import RequestContext, get_context
from ..schemas.registry import AgentRead

router = APIRouter(prefix="/agents", tags=["agents"])


def _get_agent(ctx: RequestContext, agent_id: str) -> models.Agent:
    agent = ctx.db.get(models.Agent, agent_id)
    if agent is None or agent.organization_id != ctx.org_id:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.get("", response_model=list[AgentRead])
def list_agents(ctx: RequestContext = Depends(get_context)):
    agents = ctx.db.scalars(
        select(models.Agent)
        .where(models.Agent.organization_id == ctx.org_id)
        .order_by(models.Agent.name)
    ).all()
    return [AgentRead.from_orm_agent(a) for a in agents]


@router.get("/{agent_id}", response_model=AgentRead)
def get_agent(agent_id: str, ctx: RequestContext = Depends(get_context)):
    return AgentRead.from_orm_agent(_get_agent(ctx, agent_id))


@router.get("/{agent_id}/bbom")
def get_bbom(agent_id: str, ctx: RequestContext = Depends(get_context)) -> dict:
    agent = _get_agent(ctx, agent_id)
    version = ctx.db.scalar(
        select(models.AgentVersion)
        .filter_by(agent_id=agent.id)
        .order_by(desc(models.AgentVersion.version))
    )
    if version and version.bbom:
        return version.bbom
    return (agent.metadata_ or {}).get("bbom_summary", {})

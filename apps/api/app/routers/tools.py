"""Tool registry routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from .. import models
from ..dependencies import RequestContext, get_context
from ..schemas.registry import ToolRead

router = APIRouter(prefix="/tools", tags=["tools"])


def _get_tool(ctx: RequestContext, tool_id: str) -> models.Tool:
    tool = ctx.db.get(models.Tool, tool_id)
    if tool is None or tool.organization_id != ctx.org_id:
        raise HTTPException(status_code=404, detail="Tool not found")
    return tool


@router.get("", response_model=list[ToolRead])
def list_tools(ctx: RequestContext = Depends(get_context)):
    return ctx.db.scalars(
        select(models.Tool)
        .where(models.Tool.organization_id == ctx.org_id)
        .order_by(models.Tool.name)
    ).all()


@router.get("/{tool_id}", response_model=ToolRead)
def get_tool(tool_id: str, ctx: RequestContext = Depends(get_context)):
    return _get_tool(ctx, tool_id)


@router.get("/{tool_id}/blast-radius")
def blast_radius(tool_id: str, ctx: RequestContext = Depends(get_context)) -> dict:
    tool = _get_tool(ctx, tool_id)
    external = tool.risk_level in ("high", "critical") or tool.can_delete
    capabilities = []
    if tool.can_read:
        capabilities.append("read")
    if tool.can_write:
        capabilities.append("write")
    if tool.can_delete:
        capabilities.append("delete")
    return {
        "tool_key": tool.key,
        "risk_level": tool.risk_level,
        "capabilities": capabilities,
        "external_side_effect": external,
        "requires_approval": tool.requires_approval,
        "enabled": tool.is_enabled,
        "summary": (
            f"{tool.name} can {', '.join(capabilities) or 'do nothing'}; "
            f"{'external side effects possible' if external else 'internal only'}; "
            f"{'approval required' if tool.requires_approval else 'no approval gate'}."
        ),
    }

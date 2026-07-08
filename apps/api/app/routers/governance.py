"""Governance routes — audit logs, risk summary, BBOM, policies."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import desc, func, select

from .. import models
from ..dependencies import RequestContext, get_context
from ..schemas.registry import AuditLogRead

router = APIRouter(prefix="/governance", tags=["governance"])


@router.get("/audit-logs", response_model=list[AuditLogRead])
def audit_logs(limit: int = 100, ctx: RequestContext = Depends(get_context)):
    return ctx.db.scalars(
        select(models.AuditLog)
        .where(models.AuditLog.organization_id == ctx.org_id)
        .order_by(desc(models.AuditLog.created_at))
        .limit(min(limit, 500))
    ).all()


@router.get("/risk-summary")
def risk_summary(ctx: RequestContext = Depends(get_context)) -> dict:
    tools = ctx.db.scalars(
        select(models.Tool).where(models.Tool.organization_id == ctx.org_id)
    ).all()
    tool_risk: dict[str, int] = {}
    for t in tools:
        tool_risk[t.risk_level] = tool_risk.get(t.risk_level, 0) + 1

    pending = ctx.db.scalar(
        select(func.count())
        .select_from(models.Approval)
        .where(
            models.Approval.organization_id == ctx.org_id,
            models.Approval.status == "pending",
        )
    )
    enabled_dangerous = sum(
        1 for t in tools if t.is_enabled and t.risk_level in ("high", "critical")
    )
    return {
        "tools_by_risk": tool_risk,
        "pending_approvals": int(pending or 0),
        "enabled_high_risk_tools": enabled_dangerous,
        "disabled_dangerous_tools": sum(
            1 for t in tools if not t.is_enabled and t.risk_level in ("high", "critical")
        ),
    }


@router.get("/bbom")
def bbom(ctx: RequestContext = Depends(get_context)) -> list[dict]:
    agents = ctx.db.scalars(
        select(models.Agent).where(models.Agent.organization_id == ctx.org_id)
    ).all()
    return [
        {"agent_key": a.key, "name": a.name, **(a.metadata_ or {}).get("bbom_summary", {})}
        for a in agents
    ]


@router.get("/policies")
def policies() -> list[dict]:
    return [
        {"key": "read_only_default", "title": "Default to read-only", "enforced": True},
        {"key": "mock_tools_dev", "title": "Mock tools in development", "enforced": True},
        {"key": "approval_gates", "title": "High-risk actions require human approval", "enforced": True},
        {"key": "no_secrets_to_agents", "title": "Agents never receive secrets directly", "enforced": True},
        {"key": "audit_all_side_effects", "title": "Every side effect is auditable", "enforced": True},
        {"key": "dangerous_tools_disabled", "title": "Dangerous tools disabled by default", "enforced": True},
    ]

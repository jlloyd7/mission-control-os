"""Human approval center routes."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, select

from .. import models
from ..dependencies import RequestContext, get_context
from ..schemas.registry import ApprovalDecision, ApprovalRead
from ..services import audit_service

router = APIRouter(prefix="/approvals", tags=["approvals"])


def _get_approval(ctx: RequestContext, approval_id: str) -> models.Approval:
    approval = ctx.db.get(models.Approval, approval_id)
    if approval is None or approval.organization_id != ctx.org_id:
        raise HTTPException(status_code=404, detail="Approval not found")
    return approval


@router.get("", response_model=list[ApprovalRead])
def list_approvals(ctx: RequestContext = Depends(get_context)):
    return ctx.db.scalars(
        select(models.Approval)
        .where(models.Approval.organization_id == ctx.org_id)
        .order_by(desc(models.Approval.created_at))
    ).all()


@router.get("/{approval_id}", response_model=ApprovalRead)
def get_approval(approval_id: str, ctx: RequestContext = Depends(get_context)):
    return _get_approval(ctx, approval_id)


def _decide(ctx: RequestContext, approval_id: str, status: str, reason: str | None) -> models.Approval:
    approval = _get_approval(ctx, approval_id)
    if approval.status != "pending":
        raise HTTPException(status_code=409, detail=f"Approval already {approval.status}")
    approval.status = status
    approval.decided_by_user_id = ctx.user_id
    approval.decision_reason = reason
    approval.decided_at = datetime.now(timezone.utc)
    audit_service.log_event(
        ctx.db, org_id=ctx.org_id, actor_user_id=ctx.user_id,
        event_type=f"approval.{status}", entity_type="approval", entity_id=approval.id,
        summary=f"Approval {status}: {approval.title!r}",
        payload={"reason": reason},
    )
    ctx.db.commit()
    ctx.db.refresh(approval)
    return approval


@router.post("/{approval_id}/approve", response_model=ApprovalRead)
def approve(approval_id: str, body: ApprovalDecision | None = None,
            ctx: RequestContext = Depends(get_context)):
    reason = body.reason if body else None
    return _decide(ctx, approval_id, "approved", reason)


@router.post("/{approval_id}/reject", response_model=ApprovalRead)
def reject(approval_id: str, body: ApprovalDecision | None = None,
           ctx: RequestContext = Depends(get_context)):
    reason = body.reason if body else None
    return _decide(ctx, approval_id, "rejected", reason)

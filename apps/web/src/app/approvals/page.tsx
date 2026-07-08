"use client";

import { useState } from "react";
import { ShieldAlert, ShieldCheck } from "lucide-react";

import { PageHeader } from "@/components/layout/PageHeader";
import {
  Badge,
  Button,
  Card,
  EmptyState,
  ErrorNote,
  RiskBadge,
  SectionLabel,
  Skeleton,
  StatusBadge,
} from "@/components/ui";
import { api } from "@/lib/api";
import type { Approval } from "@/lib/types";
import { useApi } from "@/lib/useApi";
import { fmtRelative, seatMeta } from "@/lib/ui";

export default function ApprovalsPage() {
  const { data, error, loading, reload } = useApi(() => api.listApprovals(), []);
  const pending = data?.filter((a) => a.status === "pending") ?? [];
  const decided = data?.filter((a) => a.status !== "pending") ?? [];

  return (
    <div>
      <PageHeader
        eyebrow={<SectionLabel>Human-in-the-loop</SectionLabel>}
        title="Approvals"
        subtitle="Every high-risk or external action pauses here for a human decision."
      />
      {error && <ErrorNote message={`Could not reach the API — is it running on ${api.base}? (${error})`} />}

      <div className="mb-2 flex items-center gap-2">
        <ShieldAlert size={15} className="text-run" />
        <span className="text-sm font-medium">Pending</span>
        <span className="mono text-[11px] text-faint">{pending.length}</span>
      </div>
      {loading ? (
        <Skeleton className="h-32" />
      ) : pending.length ? (
        <div className="grid gap-3 md:grid-cols-2">
          {pending.map((a) => (
            <ApprovalCard key={a.id} approval={a} onDone={reload} />
          ))}
        </div>
      ) : (
        <EmptyState icon={<ShieldCheck size={22} />} title="No pending approvals" hint="Risky tool actions will appear here awaiting your decision." />
      )}

      {decided.length > 0 && (
        <>
          <div className="mb-2 mt-8 flex items-center gap-2">
            <ShieldCheck size={15} className="text-muted" />
            <span className="text-sm font-medium">History</span>
          </div>
          <Card>
            <div className="divide-line">
              {decided.map((a) => (
                <div key={a.id} className="flex items-center gap-3 px-5 py-3">
                  <StatusBadge status={a.status} />
                  <div className="min-w-0 flex-1">
                    <div className="truncate text-sm">{a.title}</div>
                    {a.decision_reason && <div className="truncate text-[11px] text-faint">“{a.decision_reason}”</div>}
                  </div>
                  <span className="text-xs text-faint">{fmtRelative(a.decided_at)}</span>
                </div>
              ))}
            </div>
          </Card>
        </>
      )}
    </div>
  );
}

function ApprovalCard({ approval, onDone }: { approval: Approval; onDone: () => void }) {
  const [reason, setReason] = useState("");
  const [busy, setBusy] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const seat = approval.requested_by_agent_key ? seatMeta(approval.requested_by_agent_key) : null;

  async function decide(kind: "approve" | "reject") {
    setBusy(kind);
    setErr(null);
    try {
      if (kind === "approve") await api.approve(approval.id, reason || undefined);
      else await api.reject(approval.id, reason || undefined);
      onDone();
    } catch (e) {
      setErr(String((e as Error).message ?? e));
      setBusy(null);
    }
  }

  return (
    <Card className="flex flex-col p-5">
      <div className="flex items-start justify-between gap-3">
        <div className="text-sm font-semibold">{approval.title}</div>
        <RiskBadge level={approval.risk_level} />
      </div>
      <p className="mt-1.5 text-xs text-muted">{approval.description}</p>

      <div className="mt-3 flex flex-wrap items-center gap-2">
        {seat && <span className={`rounded border px-1.5 py-0.5 text-[10px] font-medium ${seat.chip}`}>{seat.name}</span>}
        {typeof approval.action_payload.tool === "string" && (
          <Badge tone="muted">
            <span className="mono">{approval.action_payload.tool as string}</span>
          </Badge>
        )}
      </div>

      {err && <div className="mt-3"><ErrorNote message={err} /></div>}

      <div className="mt-4 space-y-2 border-t border-line-soft pt-4">
        <input
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          placeholder="Decision reason (optional)…"
          className="focus-ring w-full rounded-lg border border-line bg-bg-2 px-3 py-2 text-xs text-text placeholder:text-faint"
        />
        <div className="flex gap-2">
          <Button variant="primary" size="sm" className="flex-1" loading={busy === "approve"} onClick={() => decide("approve")}>
            <ShieldCheck size={14} /> Approve
          </Button>
          <Button variant="danger" size="sm" className="flex-1" loading={busy === "reject"} onClick={() => decide("reject")}>
            Reject
          </Button>
        </div>
      </div>
    </Card>
  );
}

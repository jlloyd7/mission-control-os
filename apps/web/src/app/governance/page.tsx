"use client";

import { ScrollText, ShieldCheck } from "lucide-react";

import { PageHeader } from "@/components/layout/PageHeader";
import { Card, ErrorNote, SectionLabel, Skeleton, Stat } from "@/components/ui";
import { api } from "@/lib/api";
import { useApi } from "@/lib/useApi";
import { fmtRelative } from "@/lib/ui";

const POLICIES = [
  "Default to read-only",
  "Mock tools in development",
  "High-risk actions require human approval",
  "Agents never receive secrets directly",
  "Every side effect is auditable",
  "Dangerous tools disabled by default",
];

export default function GovernancePage() {
  const { data, error, loading } = useApi(
    () => Promise.all([api.riskSummary(), api.auditLogs()]),
    [],
  );
  const [risk, audit] = data ?? [];

  return (
    <div>
      <PageHeader
        eyebrow={<SectionLabel>Safety</SectionLabel>}
        title="Governance"
        subtitle="Policy, risk posture, and the full audit trail."
      />
      {error && <ErrorNote message={`Could not reach the API — is it running on ${api.base}? (${error})`} />}

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        {loading ? (
          Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-[92px]" />)
        ) : (
          <>
            <Stat label="Pending Approvals" value={risk?.pending_approvals ?? 0} tone={risk?.pending_approvals ? "run" : "ok"} />
            <Stat label="High-risk Enabled" value={risk?.enabled_high_risk_tools ?? 0} tone={risk?.enabled_high_risk_tools ? "fail" : "ok"} />
            <Stat label="Dangerous Disabled" value={risk?.disabled_dangerous_tools ?? 0} tone="ok" />
            <Stat label="Audit Events" value={audit?.length ?? 0} tone="info" />
          </>
        )}
      </div>

      <div className="mt-4 grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="p-5">
          <div className="flex items-center gap-2 text-sm font-medium">
            <ShieldCheck size={15} className="text-ok" /> Enforced Policies
          </div>
          <ul className="mt-3 space-y-2">
            {POLICIES.map((p) => (
              <li key={p} className="flex items-center gap-2 text-sm text-muted">
                <span className="status-dot text-ok" style={{ width: 6, height: 6 }} />
                {p}
              </li>
            ))}
          </ul>
        </Card>

        <Card className="lg:col-span-2">
          <div className="flex items-center gap-2 border-b border-line px-5 py-3.5 text-sm font-medium">
            <ScrollText size={15} className="text-accent" /> Audit Log
          </div>
          <div className="divide-line max-h-[520px] overflow-y-auto">
            {loading ? (
              <div className="space-y-2 p-5">
                {Array.from({ length: 6 }).map((_, i) => (
                  <Skeleton key={i} className="h-9" />
                ))}
              </div>
            ) : (
              audit?.map((log) => (
                <div key={log.id} className="flex items-center gap-3 px-5 py-2.5">
                  <div className="min-w-0 flex-1">
                    <div className="truncate text-sm text-text">{log.summary}</div>
                    <div className="mono mt-0.5 text-[10px] text-faint">
                      {log.event_type} · {log.entity_type}
                    </div>
                  </div>
                  <span className="shrink-0 text-[11px] text-faint">{fmtRelative(log.created_at)}</span>
                </div>
              ))
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}

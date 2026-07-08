"use client";

import Link from "next/link";
import {
  Activity,
  ArrowRight,
  FlaskConical,
  Plus,
  Rocket,
  ShieldAlert,
  ShieldCheck,
  Users,
} from "lucide-react";

import { PageHeader } from "@/components/layout/PageHeader";
import {
  Button,
  Card,
  EmptyState,
  ErrorNote,
  SectionLabel,
  Skeleton,
  StatusBadge,
  Stat,
} from "@/components/ui";
import { api } from "@/lib/api";
import { useApi } from "@/lib/useApi";
import { cx, fmtRelative, seatMeta } from "@/lib/ui";

export default function DashboardPage() {
  const { data, error, loading } = useApi(
    () =>
      Promise.all([
        api.listIdeas(),
        api.listMissions(),
        api.listApprovals(),
        api.listAgents(),
        api.riskSummary(),
        api.auditLogs(),
      ]),
    [],
  );

  const [ideas, missions, approvals, agents, risk, audit] = data ?? [];

  const activeMissions =
    missions?.filter((m) => ["draft", "queued", "running", "waiting_approval"].includes(m.status)) ?? [];
  const forgeReady =
    ideas?.filter((i) => i.status !== "archived" && i.status !== "promoted_to_mission") ?? [];
  const pending = approvals?.filter((a) => a.status === "pending") ?? [];

  return (
    <div>
      <PageHeader
        eyebrow={<SectionLabel>Command Center</SectionLabel>}
        title="Dashboard"
        subtitle="Turn rough ideas into agent-reviewed blueprints, then run them as governed missions."
        actions={
          <Link href="/ideas/new">
            <Button variant="primary">
              <Plus size={16} /> New Idea
            </Button>
          </Link>
        }
      />

      {error && <ErrorNote message={`Could not reach the API — is it running on ${api.base}? (${error})`} />}

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        {loading ? (
          Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-[92px]" />)
        ) : (
          <>
            <Stat label="Active Missions" value={activeMissions.length} icon={<Rocket size={16} />} tone="info" />
            <Stat label="Ideas in Forge" value={forgeReady.length} icon={<FlaskConical size={16} />} />
            <Stat
              label="Pending Approvals"
              value={pending.length}
              icon={<ShieldAlert size={16} />}
              tone={pending.length ? "run" : "muted"}
            />
            <Stat
              label="Council Seats"
              value={`${agents?.filter((a) => a.is_enabled).length ?? 0}/${agents?.length ?? 0}`}
              icon={<Users size={16} />}
              tone="ok"
              sub="agents online"
            />
          </>
        )}
      </div>

      <div className="mt-4 grid grid-cols-1 gap-4 lg:grid-cols-3">
        {/* Recent activity */}
        <Card className="lg:col-span-2">
          <div className="flex items-center justify-between border-b border-line px-5 py-3.5">
            <div className="flex items-center gap-2 text-sm font-medium">
              <Activity size={15} className="text-accent" /> Recent Activity
            </div>
            <SectionLabel>Audit trail</SectionLabel>
          </div>
          <div className="divide-line">
            {loading ? (
              <div className="space-y-2 p-5">
                {Array.from({ length: 4 }).map((_, i) => (
                  <Skeleton key={i} className="h-10" />
                ))}
              </div>
            ) : audit && audit.length > 0 ? (
              audit.slice(0, 8).map((log) => (
                <div key={log.id} className="flex items-center gap-3 px-5 py-3">
                  <span className="status-dot shrink-0 text-accent" style={{ width: 6, height: 6 }} />
                  <div className="min-w-0 flex-1">
                    <div className="truncate text-sm text-text">{log.summary}</div>
                    <div className="mono mt-0.5 text-[11px] text-faint">{log.event_type}</div>
                  </div>
                  <div className="shrink-0 text-xs text-faint">{fmtRelative(log.created_at)}</div>
                </div>
              ))
            ) : (
              <div className="p-5">
                <EmptyState title="No activity yet" hint="Create an idea and run the council to see the trail." />
              </div>
            )}
          </div>
        </Card>

        {/* Council health + risk */}
        <div className="space-y-4">
          <Card>
            <div className="border-b border-line px-5 py-3.5">
              <div className="flex items-center gap-2 text-sm font-medium">
                <Users size={15} className="text-accent" /> Council Health
              </div>
            </div>
            <div className="space-y-2 p-4">
              {loading ? (
                Array.from({ length: 3 }).map((_, i) => <Skeleton key={i} className="h-12" />)
              ) : (
                agents?.map((a) => {
                  const seat = seatMeta(a.key);
                  return (
                    <div key={a.id} className="flex items-center gap-3 rounded-lg border border-line bg-panel px-3 py-2.5">
                      <span className="status-dot" style={{ color: seat.dotVar, width: 8, height: 8 }} />
                      <div className="min-w-0 flex-1">
                        <div className="text-sm font-medium">{a.name}</div>
                        <div className="label mt-0.5">{a.persona}</div>
                      </div>
                      <span className={cx("mono text-[11px]", a.is_enabled ? "text-ok" : "text-faint")}>
                        {a.is_enabled ? "online" : "off"}
                      </span>
                    </div>
                  );
                })
              )}
            </div>
          </Card>

          <Card className="p-4">
            <div className="flex items-center gap-2 text-sm font-medium">
              <ShieldCheck size={15} className="text-ok" /> Risk Posture
            </div>
            <div className="mt-3 space-y-2 text-sm">
              <Row label="Pending approvals" value={risk?.pending_approvals ?? 0} tone={pending.length ? "run" : "ok"} />
              <Row label="Dangerous tools disabled" value={risk?.disabled_dangerous_tools ?? 0} tone="ok" />
              <Row label="High-risk tools enabled" value={risk?.enabled_high_risk_tools ?? 0} tone={risk?.enabled_high_risk_tools ? "fail" : "ok"} />
            </div>
          </Card>
        </div>
      </div>

      {/* Active missions strip */}
      <Card className="mt-4">
        <div className="flex items-center justify-between border-b border-line px-5 py-3.5">
          <div className="flex items-center gap-2 text-sm font-medium">
            <Rocket size={15} className="text-accent" /> Active Missions
          </div>
          <Link href="/missions" className="flex items-center gap-1 text-xs text-muted hover:text-accent">
            View board <ArrowRight size={13} />
          </Link>
        </div>
        <div className="p-4">
          {loading ? (
            <Skeleton className="h-16" />
          ) : activeMissions.length ? (
            <div className="grid gap-2 md:grid-cols-2">
              {activeMissions.slice(0, 4).map((m) => (
                <Link
                  key={m.id}
                  href={`/missions/${m.id}`}
                  className="card-hover flex items-center gap-3 rounded-lg border border-line bg-panel px-4 py-3"
                >
                  <div className="min-w-0 flex-1">
                    <div className="truncate text-sm font-medium">{m.title}</div>
                    <div className="mt-0.5 truncate text-xs text-muted">{m.objective}</div>
                  </div>
                  <StatusBadge status={m.status} />
                </Link>
              ))}
            </div>
          ) : (
            <EmptyState
              icon={<Rocket size={22} />}
              title="No active missions"
              hint="Promote a blueprint from the Forge to launch your first mission."
            />
          )}
        </div>
      </Card>
    </div>
  );
}

function Row({ label, value, tone }: { label: string; value: number; tone: "ok" | "run" | "fail" }) {
  const c = { ok: "text-ok", run: "text-run", fail: "text-fail" }[tone];
  return (
    <div className="flex items-center justify-between">
      <span className="text-muted">{label}</span>
      <span className={cx("mono font-medium tabular-nums", c)}>{value}</span>
    </div>
  );
}

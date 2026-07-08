"use client";

import { Ban, Bot, Check } from "lucide-react";

import { PageHeader } from "@/components/layout/PageHeader";
import { Card, ErrorNote, RiskBadge, SectionLabel, Skeleton } from "@/components/ui";
import { api } from "@/lib/api";
import type { Agent } from "@/lib/types";
import { useApi } from "@/lib/useApi";
import { cx, prettify, seatMeta } from "@/lib/ui";

export default function AgentsPage() {
  const { data: agents, error, loading } = useApi(() => api.listAgents(), []);

  return (
    <div>
      <PageHeader
        eyebrow={<SectionLabel>Council</SectionLabel>}
        title="Agents"
        subtitle="The three council seats, their model routing, and Behavioral Bill of Materials."
      />
      {error && <ErrorNote message={`Could not reach the API — is it running on ${api.base}? (${error})`} />}

      {loading ? (
        <div className="grid gap-4 md:grid-cols-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <Skeleton key={i} className="h-80" />
          ))}
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-3">
          {agents?.map((a) => (
            <AgentSeatCard key={a.id} agent={a} />
          ))}
        </div>
      )}
    </div>
  );
}

function AgentSeatCard({ agent }: { agent: Agent }) {
  const seat = seatMeta(agent.key);
  const bbom = agent.bbom as {
    can_do?: string[];
    cannot_do?: string[];
    cannot_do_without_approval?: string[];
  };
  const cannot = bbom.cannot_do ?? bbom.cannot_do_without_approval ?? [];
  const cannotLabel = bbom.cannot_do ? "Cannot do" : "Needs approval";

  return (
    <Card className={cx("flex flex-col border", seat.ring)}>
      <div className="flex items-center gap-3 border-b border-line px-5 py-4">
        <span className="status-dot" style={{ color: seat.dotVar, width: 10, height: 10 }} />
        <div className="min-w-0 flex-1">
          <div className="font-semibold">{agent.name}</div>
          <div className="label mt-0.5">{agent.persona}</div>
        </div>
        <span className={cx("mono text-[11px]", agent.is_enabled ? "text-ok" : "text-faint")}>
          {agent.is_enabled ? "online" : "off"}
        </span>
      </div>

      <div className="space-y-3 px-5 py-4">
        <div className="flex items-center justify-between text-xs">
          <span className="label">Provider</span>
          <span className="mono text-muted">{agent.provider}</span>
        </div>
        <div className="flex items-center justify-between text-xs">
          <span className="label">Model</span>
          <span className="mono truncate pl-2 text-muted">{agent.model_name}</span>
        </div>
        <div className="flex items-center justify-between text-xs">
          <span className="label">Autonomy</span>
          <span className="text-muted">{prettify(agent.autonomy_level)}</span>
        </div>
        <div className="flex items-center justify-between text-xs">
          <span className="label">Risk</span>
          <RiskBadge level={agent.risk_level} />
        </div>
      </div>

      <div className="mt-auto space-y-3 border-t border-line-soft px-5 py-4">
        {bbom.can_do && (
          <div>
            <div className="mb-1.5 flex items-center gap-1.5 text-[11px] font-medium text-ok">
              <Check size={12} /> Can do
            </div>
            <ul className="space-y-1 text-xs text-muted">
              {bbom.can_do.slice(0, 4).map((c, i) => (
                <li key={i} className="flex gap-1.5">
                  <span className="text-faint">·</span> {c}
                </li>
              ))}
            </ul>
          </div>
        )}
        {cannot.length > 0 && (
          <div>
            <div className="mb-1.5 flex items-center gap-1.5 text-[11px] font-medium text-run">
              <Ban size={12} /> {cannotLabel}
            </div>
            <ul className="space-y-1 text-xs text-muted">
              {cannot.slice(0, 3).map((c, i) => (
                <li key={i} className="flex gap-1.5">
                  <span className="text-faint">·</span> {c}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </Card>
  );
}

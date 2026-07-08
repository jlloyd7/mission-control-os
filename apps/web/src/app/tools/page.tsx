"use client";

import { Wrench } from "lucide-react";

import { PageHeader } from "@/components/layout/PageHeader";
import { Card, ErrorNote, RiskBadge, SectionLabel, Skeleton } from "@/components/ui";
import { api } from "@/lib/api";
import type { Tool } from "@/lib/types";
import { useApi } from "@/lib/useApi";
import { cx } from "@/lib/ui";

export default function ToolsPage() {
  const { data: tools, error, loading } = useApi(() => api.listTools(), []);

  return (
    <div>
      <PageHeader
        eyebrow={<SectionLabel>Governance</SectionLabel>}
        title="Tools"
        subtitle="The tool registry with permissions, risk, and approval gates. Dangerous tools are disabled by default."
      />
      {error && <ErrorNote message={`Could not reach the API — is it running on ${api.base}? (${error})`} />}

      <Card>
        <div className="hidden grid-cols-[1.6fr_1fr_1fr_0.8fr_0.8fr] gap-4 border-b border-line px-5 py-3 md:grid">
          <SectionLabel>Tool</SectionLabel>
          <SectionLabel>Capabilities</SectionLabel>
          <SectionLabel>Approval</SectionLabel>
          <SectionLabel>Risk</SectionLabel>
          <SectionLabel>Status</SectionLabel>
        </div>
        <div className="divide-line">
          {loading
            ? Array.from({ length: 6 }).map((_, i) => <div key={i} className="p-4"><Skeleton className="h-8" /></div>)
            : tools?.map((t) => <ToolRow key={t.id} tool={t} />)}
        </div>
      </Card>
    </div>
  );
}

function ToolRow({ tool }: { tool: Tool }) {
  return (
    <div className="grid grid-cols-1 gap-3 px-5 py-4 md:grid-cols-[1.6fr_1fr_1fr_0.8fr_0.8fr] md:items-center">
      <div className="flex items-center gap-3">
        <div className="grid h-8 w-8 shrink-0 place-items-center rounded-lg border border-line bg-panel">
          <Wrench size={15} className="text-faint" />
        </div>
        <div className="min-w-0">
          <div className="text-sm font-medium">{tool.name}</div>
          <div className="mono text-[11px] text-faint">{tool.key}</div>
        </div>
      </div>

      <div className="flex flex-wrap gap-1.5">
        <Cap active={tool.can_read} label="R" tone="ok" title="read" />
        <Cap active={tool.can_write} label="W" tone="run" title="write" />
        <Cap active={tool.can_delete} label="D" tone="fail" title="delete" />
      </div>

      <div>
        {tool.requires_approval ? (
          <span className="mono text-xs text-run">required</span>
        ) : (
          <span className="mono text-xs text-faint">none</span>
        )}
      </div>

      <div><RiskBadge level={tool.risk_level} /></div>

      <div className="flex items-center gap-1.5">
        <span className={cx("status-dot", tool.is_enabled ? "text-ok" : "text-faint")} style={{ width: 6, height: 6 }} />
        <span className={cx("mono text-xs", tool.is_enabled ? "text-ok" : "text-faint")}>
          {tool.is_enabled ? "enabled" : "disabled"}
        </span>
      </div>
    </div>
  );
}

function Cap({ active, label, tone, title }: { active: boolean; label: string; tone: "ok" | "run" | "fail"; title: string }) {
  const cls = active
    ? { ok: "border-ok/30 text-ok bg-ok/10", run: "border-run/30 text-run bg-run/10", fail: "border-fail/30 text-fail bg-fail/10" }[tone]
    : "border-line text-faint/50 bg-transparent";
  return (
    <span title={title} className={cx("mono grid h-6 w-6 place-items-center rounded border text-[11px] font-semibold", cls)}>
      {label}
    </span>
  );
}

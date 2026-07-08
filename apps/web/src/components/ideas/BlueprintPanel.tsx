"use client";

import { FileText, GitBranch, ListChecks, Route, ShieldCheck } from "lucide-react";

import { Card } from "@/components/ui";
import type { Blueprint } from "@/lib/types";
import { cx } from "@/lib/ui";

const PRIORITY_CLASS: Record<string, string> = {
  P0: "bg-fail/10 text-fail border-fail/25",
  P1: "bg-run/10 text-run border-run/25",
  P2: "bg-info/10 text-info border-info/25",
  Future: "bg-white/5 text-muted border-line",
};

export function BlueprintPanel({ blueprint }: { blueprint: Blueprint }) {
  return (
    <Card>
      <div className="flex items-center justify-between border-b border-line px-5 py-3.5">
        <div className="flex items-center gap-2 text-sm font-medium">
          <FileText size={15} className="text-accent" /> Blueprint
        </div>
        {blueprint.readiness_score != null && (
          <span className="mono text-xs text-ok">readiness {blueprint.readiness_score}%</span>
        )}
      </div>

      <div className="space-y-5 p-5">
        <p className="text-sm text-muted">{blueprint.summary}</p>

        <Section icon={<ListChecks size={14} />} title={`Features (${blueprint.feature_list.length})`}>
          <div className="space-y-2">
            {blueprint.feature_list.map((f, i) => (
              <div key={i} className="rounded-lg border border-line bg-panel px-3 py-2.5">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-sm font-medium">{f.name}</span>
                  <span className={cx("rounded border px-1.5 py-0.5 text-[10px] font-semibold", PRIORITY_CLASS[f.priority] ?? PRIORITY_CLASS.Future)}>
                    {f.priority}
                  </span>
                </div>
                <p className="mt-1 text-xs text-muted">{f.description}</p>
              </div>
            ))}
          </div>
        </Section>

        <Section icon={<Route size={14} />} title="User flow">
          <ol className="flex flex-wrap items-center gap-1.5">
            {blueprint.user_flow.map((step, i) => (
              <li key={i} className="flex items-center gap-1.5">
                <span className="rounded-md border border-line bg-bg-2 px-2 py-1 text-[11px] text-muted">{step}</span>
                {i < blueprint.user_flow.length - 1 && <span className="text-faint">›</span>}
              </li>
            ))}
          </ol>
        </Section>

        <div className="grid gap-5 sm:grid-cols-2">
          <Section icon={<ShieldCheck size={14} />} title="Risk controls">
            <ul className="list-disc space-y-1 pl-4 text-xs text-muted">
              {blueprint.risk_controls.map((r, i) => (
                <li key={i}>{r}</li>
              ))}
            </ul>
          </Section>
          <Section icon={<GitBranch size={14} />} title="Architecture">
            <dl className="space-y-1 text-xs">
              {Object.entries(blueprint.technical_architecture).map(([k, v]) => (
                <div key={k} className="flex gap-2">
                  <dt className="mono w-24 shrink-0 text-faint">{k}</dt>
                  <dd className="text-muted">{Array.isArray(v) ? v.join(", ") : String(v)}</dd>
                </div>
              ))}
            </dl>
          </Section>
        </div>

        {blueprint.lineage.length > 0 && (
          <Section icon={<GitBranch size={14} />} title="Lineage">
            <div className="space-y-1">
              {blueprint.lineage.map((l, i) => (
                <div key={i} className="flex items-center gap-2 text-xs text-muted">
                  <span className="status-dot text-accent" style={{ width: 5, height: 5 }} />
                  <span className="truncate">{String(l.part)}</span>
                  <span className="mono ml-auto shrink-0 text-[10px] text-faint">{String(l.source_agent)}</span>
                </div>
              ))}
            </div>
          </Section>
        )}
      </div>
    </Card>
  );
}

function Section({ icon, title, children }: { icon: React.ReactNode; title: string; children: React.ReactNode }) {
  return (
    <div>
      <div className="mb-2 flex items-center gap-2 text-xs font-medium text-text">
        <span className="text-faint">{icon}</span>
        {title}
      </div>
      {children}
    </div>
  );
}

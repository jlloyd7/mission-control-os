"use client";

import { useState } from "react";
import { ChevronDown, ListChecks, ShieldAlert, Sparkles } from "lucide-react";

import { Card } from "@/components/ui";
import type { AgentKey, CouncilContribution, CouncilRun } from "@/lib/types";
import { cx, seatMeta } from "@/lib/ui";

const ORDER: AgentKey[] = ["george", "cipher_fable", "arty_codex"];

export function CouncilRoom({ run, running }: { run: CouncilRun | null; running?: boolean }) {
  const byKey = new Map((run?.contributions ?? []).map((c) => [c.agent_key, c]));

  return (
    <Card>
      <div className="flex items-center justify-between border-b border-line px-5 py-3.5">
        <div className="flex items-center gap-2 text-sm font-medium">
          <Sparkles size={15} className="text-accent" /> Council Room
        </div>
        <span className="label">Triad</span>
      </div>
      <div className="space-y-3 p-4">
        {ORDER.map((key) => (
          <SeatCard key={key} seatKey={key} contribution={byKey.get(key) ?? null} running={running} />
        ))}
      </div>
    </Card>
  );
}

function SeatCard({
  seatKey,
  contribution,
  running,
}: {
  seatKey: string;
  contribution: CouncilContribution | null;
  running?: boolean;
}) {
  const [open, setOpen] = useState(false);
  const seat = seatMeta(seatKey);
  const p = contribution?.content;
  const status = contribution ? "complete" : running ? "running" : "waiting";

  return (
    <div className={cx("rounded-xl border bg-panel", contribution ? seat.ring : "border-line")}>
      <button
        onClick={() => contribution && setOpen((v) => !v)}
        className="flex w-full items-center gap-3 px-4 py-3 text-left"
        disabled={!contribution}
      >
        <span className="status-dot" style={{ color: seat.dotVar, width: 9, height: 9 }} />
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2">
            <span className="text-sm font-semibold">{seat.name}</span>
            <span className={cx("rounded border px-1.5 py-0.5 text-[10px] font-medium", seat.chip)}>
              {seat.role}
            </span>
          </div>
          <div className="mt-0.5 truncate text-xs text-muted">
            {contribution ? contribution.title : status === "running" ? "Deliberating…" : "Awaiting council run"}
          </div>
        </div>
        {contribution ? (
          <div className="flex items-center gap-3 text-right">
            <div>
              <div className="label">Conf</div>
              <div className="mono text-sm font-medium tabular-nums text-text">
                {Math.round((contribution.confidence ?? 0) * 100)}%
              </div>
            </div>
            <ChevronDown size={16} className={cx("text-faint transition", open && "rotate-180")} />
          </div>
        ) : (
          <span className={cx("mono text-[11px]", status === "running" ? "animate-pulse-dot text-run" : "text-faint")}>
            {status}
          </span>
        )}
      </button>

      {open && p && (
        <div className="space-y-3 border-t border-line-soft px-4 py-3.5 text-sm">
          <p className="text-muted">{p.summary}</p>
          <div className="flex flex-wrap gap-2">
            <Chip icon={<Sparkles size={12} />} label={`${p.best_features.length} best features`} />
            <Chip icon={<ShieldAlert size={12} />} label={`${p.risks.length} risks`} />
            <Chip icon={<ListChecks size={12} />} label={`${p.build_steps.length} build steps`} />
          </div>
          {p.proposal && (
            <Detail label="Proposal">{p.proposal}</Detail>
          )}
          {p.risks.length > 0 && (
            <Detail label="Risks">
              <ul className="list-disc space-y-0.5 pl-4">
                {p.risks.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            </Detail>
          )}
          {p.human_approval_needed.length > 0 && (
            <Detail label="Human approval needed">
              <ul className="list-disc space-y-0.5 pl-4 text-run">
                {p.human_approval_needed.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            </Detail>
          )}
        </div>
      )}
    </div>
  );
}

function Chip({ icon, label }: { icon: React.ReactNode; label: string }) {
  return (
    <span className="inline-flex items-center gap-1.5 rounded-md border border-line bg-bg-2 px-2 py-1 text-[11px] text-muted">
      <span className="text-faint">{icon}</span>
      {label}
    </span>
  );
}

function Detail({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <div className="label mb-1">{label}</div>
      <div className="text-[13px] text-muted">{children}</div>
    </div>
  );
}

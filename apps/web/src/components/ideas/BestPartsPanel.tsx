"use client";

import { Layers } from "lucide-react";

import { Badge, Card, EmptyState } from "@/components/ui";
import type { BestPart } from "@/lib/types";
import { cx, decisionMeta, seatMeta, TONE_CHIP } from "@/lib/ui";

const GROUPS = [
  { key: "keep", label: "Keep" },
  { key: "modify", label: "Modify" },
  { key: "needs_human_approval", label: "Needs Approval" },
  { key: "needs_evidence", label: "Needs Evidence" },
  { key: "reject", label: "Reject" },
];

export function BestPartsPanel({ parts }: { parts: BestPart[] }) {
  return (
    <Card>
      <div className="flex items-center justify-between border-b border-line px-5 py-3.5">
        <div className="flex items-center gap-2 text-sm font-medium">
          <Layers size={15} className="text-accent" /> Best Parts
        </div>
        <span className="label">{parts.length} fragments</span>
      </div>

      {parts.length === 0 ? (
        <div className="p-5">
          <EmptyState title="No best parts yet" hint="Run Extract Best Parts to score and bucket the council's fragments." />
        </div>
      ) : (
        <div className="space-y-5 p-4">
          {GROUPS.map((g) => {
            const items = parts.filter((p) => p.decision === g.key);
            if (items.length === 0) return null;
            const meta = decisionMeta(g.key);
            return (
              <div key={g.key}>
                <div className="mb-2 flex items-center gap-2">
                  <span className={cx("inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium", TONE_CHIP[meta.tone])}>
                    {meta.label}
                  </span>
                  <span className="mono text-[11px] text-faint">{items.length}</span>
                </div>
                <div className="space-y-2">
                  {items.map((p) => (
                    <FragmentRow key={p.id} part={p} />
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </Card>
  );
}

function FragmentRow({ part }: { part: BestPart }) {
  const seat = seatMeta(part.source_agent_key);
  return (
    <div className="rounded-lg border border-line bg-panel px-4 py-3">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <span className={cx("rounded border px-1.5 py-0.5 text-[10px] font-medium", seat.chip)}>
              {seat.name}
            </span>
            <span className="mono text-[10px] uppercase tracking-wide text-faint">{part.part_type}</span>
          </div>
          <div className="mt-1.5 text-sm font-medium">{part.title}</div>
        </div>
        <div className="shrink-0 text-right">
          <div className="label">Score</div>
          <div className="mono text-sm font-semibold tabular-nums text-accent">
            {part.weighted_score ?? "—"}
          </div>
        </div>
      </div>
      <p className="mt-1.5 text-xs text-muted">{part.summary}</p>
      {part.rationale && (
        <p className="mt-1.5 border-l-2 border-line pl-2 text-[11px] italic text-faint">{part.rationale}</p>
      )}
    </div>
  );
}

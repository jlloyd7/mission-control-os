"use client";

import {
  AlertTriangle,
  Boxes,
  Brain,
  CheckCircle2,
  FileText,
  Layers,
  Package,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  User,
  Wrench,
} from "lucide-react";

import { EmptyState } from "@/components/ui";
import type { RunStep } from "@/lib/types";
import { cx, fmtDate, seatMeta } from "@/lib/ui";

const STEP_META: Record<string, { icon: typeof User; tone: string }> = {
  user_input: { icon: User, tone: "text-muted" },
  agent_proposal: { icon: Sparkles, tone: "text-accent" },
  agent_thought_summary: { icon: Brain, tone: "text-cipher" },
  tool_call: { icon: Wrench, tone: "text-info" },
  tool_result: { icon: CheckCircle2, tone: "text-ok" },
  best_parts_extraction: { icon: Layers, tone: "text-accent" },
  blueprint_generation: { icon: FileText, tone: "text-accent" },
  approval_request: { icon: ShieldAlert, tone: "text-run" },
  approval_decision: { icon: ShieldCheck, tone: "text-ok" },
  artifact_created: { icon: Package, tone: "text-arty" },
  error: { icon: AlertTriangle, tone: "text-fail" },
};

export function RunTimeline({ steps }: { steps: RunStep[] }) {
  if (!steps.length) {
    return <EmptyState icon={<Boxes size={22} />} title="No steps yet" hint="Start a run to populate the timeline." />;
  }

  return (
    <ol className="relative space-y-1">
      <div className="absolute bottom-4 left-[13px] top-4 w-px bg-line" aria-hidden />
      {steps.map((step) => {
        const meta = STEP_META[step.step_type] ?? { icon: Boxes, tone: "text-muted" };
        const Icon = meta.icon;
        const seat = step.agent_key ? seatMeta(step.agent_key) : null;
        const failed = step.status === "failed";
        return (
          <li key={step.id} className="relative flex gap-3 py-2">
            <div
              className={cx(
                "z-[1] grid h-7 w-7 shrink-0 place-items-center rounded-full border bg-panel",
                failed ? "border-fail/40" : "border-line",
              )}
            >
              <Icon size={14} className={failed ? "text-fail" : meta.tone} />
            </div>
            <div className="min-w-0 flex-1 pb-1">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium">{step.title}</span>
                {seat && (
                  <span className={cx("rounded border px-1.5 py-0.5 text-[10px] font-medium", seat.chip)}>
                    {seat.name}
                  </span>
                )}
                <span className="mono ml-auto shrink-0 text-[10px] text-faint">{fmtDate(step.created_at)}</span>
              </div>
              {step.summary && <p className="mt-0.5 text-xs text-muted">{step.summary}</p>}
              {step.error_message && <p className="mt-0.5 text-xs text-fail">{step.error_message}</p>}
            </div>
          </li>
        );
      })}
    </ol>
  );
}

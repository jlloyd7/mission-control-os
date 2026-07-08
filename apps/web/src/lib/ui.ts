import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cx(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export type Tone = "ok" | "run" | "fail" | "pending" | "info" | "muted";

// Literal class strings so Tailwind can detect them.
export const TONE_CHIP: Record<Tone, string> = {
  ok: "bg-ok/10 text-ok border-ok/25",
  run: "bg-run/10 text-run border-run/25",
  fail: "bg-fail/10 text-fail border-fail/25",
  pending: "bg-pending/10 text-pending border-pending/25",
  info: "bg-info/10 text-info border-info/25",
  muted: "bg-white/5 text-muted border-line",
};

export const TONE_TEXT: Record<Tone, string> = {
  ok: "text-ok",
  run: "text-run",
  fail: "text-fail",
  pending: "text-pending",
  info: "text-info",
  muted: "text-muted",
};

const STATUS_MAP: Record<string, { label: string; tone: Tone }> = {
  raw: { label: "Raw Idea", tone: "muted" },
  council_ready: { label: "Council Ready", tone: "info" },
  council_running: { label: "Council Running", tone: "run" },
  council_complete: { label: "Council Complete", tone: "ok" },
  best_parts_extracted: { label: "Best Parts", tone: "info" },
  blueprint_ready: { label: "Blueprint Ready", tone: "info" },
  promoted_to_mission: { label: "Promoted", tone: "ok" },
  archived: { label: "Archived", tone: "muted" },
  draft: { label: "Draft", tone: "muted" },
  queued: { label: "Queued", tone: "pending" },
  running: { label: "Running", tone: "run" },
  paused: { label: "Paused", tone: "pending" },
  blocked: { label: "Blocked", tone: "fail" },
  waiting_approval: { label: "Waiting Approval", tone: "run" },
  completed: { label: "Completed", tone: "ok" },
  failed: { label: "Failed", tone: "fail" },
  cancelled: { label: "Cancelled", tone: "muted" },
  pending: { label: "Pending", tone: "pending" },
  approved: { label: "Approved", tone: "ok" },
  rejected: { label: "Rejected", tone: "fail" },
  expired: { label: "Expired", tone: "muted" },
};

export function statusMeta(status: string): { label: string; tone: Tone } {
  return STATUS_MAP[status] ?? { label: prettify(status), tone: "muted" };
}

export const RISK_CHIP: Record<string, string> = {
  low: "bg-risk-low/10 text-risk-low border-risk-low/25",
  medium: "bg-risk-medium/10 text-risk-medium border-risk-medium/25",
  high: "bg-risk-high/10 text-risk-high border-risk-high/25",
  critical: "bg-risk-critical/10 text-risk-critical border-risk-critical/25",
};

export interface SeatMeta {
  name: string;
  role: string;
  text: string;
  chip: string;
  ring: string;
  dotVar: string;
}

export const SEATS: Record<string, SeatMeta> = {
  george: {
    name: "George",
    role: "Commander",
    text: "text-george",
    chip: "bg-george/10 text-george border-george/25",
    ring: "border-george/30",
    dotVar: "var(--color-george)",
  },
  cipher_fable: {
    name: "Cipher",
    role: "Sentinel",
    text: "text-cipher",
    chip: "bg-cipher/10 text-cipher border-cipher/25",
    ring: "border-cipher/30",
    dotVar: "var(--color-cipher)",
  },
  arty_codex: {
    name: "Arty",
    role: "Maker",
    text: "text-arty",
    chip: "bg-arty/10 text-arty border-arty/25",
    ring: "border-arty/30",
    dotVar: "var(--color-arty)",
  },
};

export function seatMeta(key: string): SeatMeta {
  return SEATS[key] ?? { name: key, role: "Agent", text: "text-muted", chip: TONE_CHIP.muted, ring: "border-line", dotVar: "var(--color-muted)" };
}

const DECISION_MAP: Record<string, { label: string; tone: Tone }> = {
  keep: { label: "Keep", tone: "ok" },
  modify: { label: "Modify", tone: "info" },
  needs_human_approval: { label: "Needs Approval", tone: "run" },
  needs_evidence: { label: "Needs Evidence", tone: "pending" },
  reject: { label: "Reject", tone: "fail" },
};

export function decisionMeta(decision: string): { label: string; tone: Tone } {
  return DECISION_MAP[decision] ?? { label: prettify(decision), tone: "muted" };
}

export function prettify(s: string): string {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export function shortId(id: string): string {
  return id.slice(0, 8);
}

export function fmtDate(iso: string | null): string {
  if (!iso) return "—";
  return new Date(iso).toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function fmtRelative(iso: string | null): string {
  if (!iso) return "—";
  const then = new Date(iso).getTime();
  const diff = Date.now() - then;
  const mins = Math.round(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.round(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.round(hrs / 24);
  return `${days}d ago`;
}

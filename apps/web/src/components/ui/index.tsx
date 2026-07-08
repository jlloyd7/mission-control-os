"use client";

import type { ButtonHTMLAttributes, ReactNode } from "react";
import { Loader2 } from "lucide-react";

import { cx, RISK_CHIP, statusMeta, TONE_CHIP, type Tone } from "@/lib/ui";

export function Card({
  className,
  children,
  hover = false,
}: {
  className?: string;
  children: ReactNode;
  hover?: boolean;
}) {
  return <div className={cx("panel", hover && "card-hover", className)}>{children}</div>;
}

export function SectionLabel({ children, className }: { children: ReactNode; className?: string }) {
  return <div className={cx("label", className)}>{children}</div>;
}

export function Badge({
  children,
  tone = "muted",
  className,
}: {
  children: ReactNode;
  tone?: Tone;
  className?: string;
}) {
  return (
    <span
      className={cx(
        "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium",
        TONE_CHIP[tone],
        className,
      )}
    >
      {children}
    </span>
  );
}

export function StatusBadge({ status, dot = true }: { status: string; dot?: boolean }) {
  const m = statusMeta(status);
  return (
    <span
      className={cx(
        "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium",
        TONE_CHIP[m.tone],
      )}
    >
      {dot && (
        <span
          className={cx("status-dot", m.tone === "run" && "animate-pulse-dot")}
          style={{ width: 6, height: 6 }}
        />
      )}
      {m.label}
    </span>
  );
}

export function RiskBadge({ level }: { level: string }) {
  return (
    <span
      className={cx(
        "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium capitalize",
        RISK_CHIP[level] ?? TONE_CHIP.muted,
      )}
    >
      {level}
    </span>
  );
}

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "ghost" | "danger";
  size?: "sm" | "md";
  loading?: boolean;
};

export function Button({
  variant = "secondary",
  size = "md",
  loading = false,
  disabled,
  className,
  children,
  ...props
}: ButtonProps) {
  const base =
    "inline-flex items-center justify-center gap-2 rounded-lg font-medium transition focus-ring disabled:opacity-45 disabled:cursor-not-allowed select-none";
  const sizes = { sm: "h-8 px-3 text-xs", md: "h-9 px-4 text-sm" };
  const variants = {
    primary: "bg-accent text-bg font-semibold hover:bg-accent/90 shadow-[0_0_20px_-6px_var(--color-accent)]",
    secondary: "bg-panel border border-line text-text hover:border-accent/40 hover:bg-panel-2",
    ghost: "text-muted hover:text-text hover:bg-white/5",
    danger: "bg-fail/15 text-fail border border-fail/30 hover:bg-fail/25",
  };
  return (
    <button
      className={cx(base, sizes[size], variants[variant], className)}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <Loader2 className="animate-spin" size={size === "sm" ? 13 : 15} />}
      {children}
    </button>
  );
}

export function Stat({
  label,
  value,
  sub,
  icon,
  tone = "muted",
}: {
  label: string;
  value: ReactNode;
  sub?: ReactNode;
  icon?: ReactNode;
  tone?: Tone;
}) {
  const toneText = {
    ok: "text-ok",
    run: "text-run",
    fail: "text-fail",
    pending: "text-pending",
    info: "text-info",
    muted: "text-text",
  }[tone];
  return (
    <Card className="p-4">
      <div className="flex items-start justify-between">
        <SectionLabel>{label}</SectionLabel>
        {icon && <span className="text-faint">{icon}</span>}
      </div>
      <div className={cx("mt-2 text-2xl font-semibold tracking-tight tabular-nums", toneText)}>
        {value}
      </div>
      {sub && <div className="mt-0.5 text-xs text-muted">{sub}</div>}
    </Card>
  );
}

export function EmptyState({
  icon,
  title,
  hint,
  action,
}: {
  icon?: ReactNode;
  title: string;
  hint?: string;
  action?: ReactNode;
}) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 rounded-xl border border-dashed border-line px-6 py-14 text-center">
      {icon && <div className="text-faint">{icon}</div>}
      <div className="text-sm font-medium text-text">{title}</div>
      {hint && <div className="max-w-sm text-xs text-muted">{hint}</div>}
      {action}
    </div>
  );
}

export function ErrorNote({ message }: { message: string }) {
  return (
    <div className="rounded-lg border border-fail/30 bg-fail/10 px-3 py-2 text-xs text-fail">
      {message}
    </div>
  );
}

export function Meter({ value, tone = "ok" }: { value: number; tone?: Tone }) {
  const bar = {
    ok: "bg-ok",
    run: "bg-run",
    fail: "bg-fail",
    pending: "bg-pending",
    info: "bg-info",
    muted: "bg-muted",
  }[tone];
  return (
    <div className="h-1.5 w-full overflow-hidden rounded-full bg-white/5">
      <div className={cx("h-full rounded-full", bar)} style={{ width: `${Math.max(0, Math.min(100, value))}%` }} />
    </div>
  );
}

export function Skeleton({ className }: { className?: string }) {
  return <div className={cx("skeleton rounded-lg", className)} />;
}

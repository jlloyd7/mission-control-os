"use client";

import Link from "next/link";
import { FlaskConical, Plus } from "lucide-react";

import { PageHeader } from "@/components/layout/PageHeader";
import {
  Button,
  Card,
  EmptyState,
  ErrorNote,
  SectionLabel,
  Skeleton,
  StatusBadge,
} from "@/components/ui";
import { api } from "@/lib/api";
import { useApi } from "@/lib/useApi";
import { fmtRelative } from "@/lib/ui";

export default function IdeasPage() {
  const { data: ideas, error, loading } = useApi(() => api.listIdeas(), []);
  const visible = ideas?.filter((i) => i.status !== "archived") ?? [];

  return (
    <div>
      <PageHeader
        eyebrow={<SectionLabel>Forge</SectionLabel>}
        title="Ideas"
        subtitle="Capture raw ideas and evolve them into agent-reviewed blueprints."
        actions={
          <Link href="/ideas/new">
            <Button variant="primary">
              <Plus size={16} /> New Idea
            </Button>
          </Link>
        }
      />

      {error && <ErrorNote message={`Could not reach the API — is it running on ${api.base}? (${error})`} />}

      {loading ? (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <Skeleton key={i} className="h-44" />
          ))}
        </div>
      ) : visible.length ? (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {visible.map((idea) => (
            <Link key={idea.id} href={`/ideas/${idea.id}`}>
              <Card hover className="flex h-full flex-col p-5">
                <div className="flex items-start justify-between gap-3">
                  <h3 className="font-semibold leading-snug tracking-tight">{idea.title}</h3>
                  <StatusBadge status={idea.status} />
                </div>
                <p className="mt-2 line-clamp-2 flex-1 text-sm text-muted">{idea.seed_prompt}</p>

                {idea.tags.length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {idea.tags.slice(0, 4).map((t) => (
                      <span key={t} className="mono rounded-md border border-line bg-panel px-1.5 py-0.5 text-[10px] text-muted">
                        {t}
                      </span>
                    ))}
                  </div>
                )}

                <div className="mt-4 grid grid-cols-3 gap-2 border-t border-line-soft pt-3">
                  <Metric label="Idea" value={idea.idea_score} />
                  <Metric label="Risk" value={idea.risk_score} />
                  <Metric label="Ready" value={idea.readiness_score} suffix={idea.readiness_score != null ? "%" : ""} />
                </div>
                <div className="mono mt-3 text-[11px] text-faint">updated {fmtRelative(idea.updated_at)}</div>
              </Card>
            </Link>
          ))}
        </div>
      ) : (
        <EmptyState
          icon={<FlaskConical size={24} />}
          title="No ideas yet"
          hint="Every mission starts as a raw idea. Capture your first one to summon the council."
          action={
            <Link href="/ideas/new">
              <Button variant="primary">
                <Plus size={16} /> New Idea
              </Button>
            </Link>
          }
        />
      )}
    </div>
  );
}

function Metric({ label, value, suffix = "" }: { label: string; value: number | null; suffix?: string }) {
  return (
    <div>
      <div className="label">{label}</div>
      <div className="mono mt-1 text-sm font-medium tabular-nums text-text">
        {value != null ? `${value}${suffix}` : "—"}
      </div>
    </div>
  );
}

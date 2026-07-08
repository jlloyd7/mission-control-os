"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowLeft, Activity } from "lucide-react";

import { RunTimeline } from "@/components/missions/RunTimeline";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, ErrorNote, SectionLabel, Skeleton, Stat, StatusBadge } from "@/components/ui";
import { api } from "@/lib/api";
import { useApi } from "@/lib/useApi";
import { fmtDate } from "@/lib/ui";

export default function RunDetailPage() {
  const { runId } = useParams<{ runId: string }>();
  const { data: run, error, loading } = useApi(() => api.getRun(runId), [runId]);

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-56" />
        <div className="grid grid-cols-3 gap-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <Skeleton key={i} className="h-20" />
          ))}
        </div>
        <Skeleton className="h-80" />
      </div>
    );
  }
  if (error || !run) return <ErrorNote message={`Could not load run (${error ?? "not found"}).`} />;

  return (
    <div>
      <PageHeader
        eyebrow={
          <Link href={`/missions/${run.mission_id}`} className="flex items-center gap-1 text-xs text-muted hover:text-accent">
            <ArrowLeft size={13} /> Mission
          </Link>
        }
        title={
          <span className="flex items-center gap-3">
            Run Timeline
            <StatusBadge status={run.status} />
          </span>
        }
        subtitle={`Run mode: ${run.run_mode} · started ${fmtDate(run.started_at)}`}
      />

      <div className="mb-4 grid grid-cols-2 gap-4 md:grid-cols-4">
        <Stat label="Input tokens" value={run.total_input_tokens} />
        <Stat label="Output tokens" value={run.total_output_tokens} />
        <Stat label="Est. cost" value={`$${run.estimated_cost_usd.toFixed(2)}`} />
        <Stat label="Steps" value={run.steps?.length ?? 0} tone="info" />
      </div>

      <Card>
        <div className="flex items-center gap-2 border-b border-line px-5 py-3.5 text-sm font-medium">
          <Activity size={15} className="text-accent" /> Steps
        </div>
        <div className="p-5">
          <RunTimeline steps={run.steps ?? []} />
        </div>
      </Card>
    </div>
  );
}

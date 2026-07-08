"use client";

import Link from "next/link";
import { Rocket } from "lucide-react";

import { PageHeader } from "@/components/layout/PageHeader";
import { EmptyState, ErrorNote, RiskBadge, SectionLabel, Skeleton } from "@/components/ui";
import { api } from "@/lib/api";
import type { Mission } from "@/lib/types";
import { useApi } from "@/lib/useApi";
import { fmtRelative, statusMeta, TONE_TEXT } from "@/lib/ui";

const COLUMNS = [
  { key: "draft", label: "Draft" },
  { key: "queued", label: "Queued" },
  { key: "running", label: "Running" },
  { key: "waiting_approval", label: "Waiting Approval" },
  { key: "completed", label: "Completed" },
  { key: "failed", label: "Failed" },
];

export default function MissionsPage() {
  const { data: missions, error, loading } = useApi(() => api.listMissions(), []);

  return (
    <div>
      <PageHeader
        eyebrow={<SectionLabel>Mission Control</SectionLabel>}
        title="Missions"
        subtitle="Track blueprints executing as governed missions."
      />

      {error && <ErrorNote message={`Could not reach the API — is it running on ${api.base}? (${error})`} />}

      {loading ? (
        <div className="grid gap-4 md:grid-cols-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <Skeleton key={i} className="h-40" />
          ))}
        </div>
      ) : missions && missions.length > 0 ? (
        <div className="flex gap-4 overflow-x-auto pb-4">
          {COLUMNS.map((col) => {
            const items = missions.filter((m) => m.status === col.key);
            const tone = statusMeta(col.key).tone;
            return (
              <div key={col.key} className="w-72 shrink-0">
                <div className="mb-2 flex items-center gap-2 px-1">
                  <span className={`status-dot ${TONE_TEXT[tone]}`} style={{ width: 7, height: 7 }} />
                  <span className="text-sm font-medium">{col.label}</span>
                  <span className="mono ml-auto text-[11px] text-faint">{items.length}</span>
                </div>
                <div className="space-y-2">
                  {items.map((m) => (
                    <MissionCard key={m.id} mission={m} />
                  ))}
                  {items.length === 0 && (
                    <div className="rounded-lg border border-dashed border-line px-3 py-6 text-center text-[11px] text-faint">
                      empty
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <EmptyState
          icon={<Rocket size={24} />}
          title="No missions yet"
          hint="Promote a blueprint from the Forge to create your first mission."
          action={
            <Link href="/ideas" className="text-sm text-accent hover:underline">
              Go to the Forge →
            </Link>
          }
        />
      )}
    </div>
  );
}

function MissionCard({ mission }: { mission: Mission }) {
  return (
    <Link href={`/missions/${mission.id}`}>
      <div className="card-hover rounded-lg border border-line bg-panel p-3.5">
        <div className="flex items-start justify-between gap-2">
          <div className="text-sm font-medium leading-snug">{mission.title}</div>
          <RiskBadge level={mission.risk_level} />
        </div>
        <p className="mt-1.5 line-clamp-2 text-xs text-muted">{mission.objective}</p>
        <div className="mono mt-2.5 text-[10px] text-faint">updated {fmtRelative(mission.updated_at)}</div>
      </div>
    </Link>
  );
}

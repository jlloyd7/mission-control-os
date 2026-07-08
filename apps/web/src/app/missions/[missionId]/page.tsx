"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useState } from "react";
import { ArrowLeft, FileText, Lightbulb, Play, Rocket } from "lucide-react";

import { RunTimeline } from "@/components/missions/RunTimeline";
import { PageHeader } from "@/components/layout/PageHeader";
import {
  Button,
  Card,
  ErrorNote,
  RiskBadge,
  SectionLabel,
  Skeleton,
  StatusBadge,
} from "@/components/ui";
import { api } from "@/lib/api";
import { useApi } from "@/lib/useApi";
import { fmtDate, shortId } from "@/lib/ui";

export default function MissionDetailPage() {
  const { missionId } = useParams<{ missionId: string }>();
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const { data, error, loading, reload } = useApi(async () => {
    const mission = await api.getMission(missionId);
    const latest = mission.runs?.[0];
    const runDetail = latest ? await api.getRun(latest.id) : null;
    return { mission, runDetail };
  }, [missionId]);

  async function startRun() {
    setBusy(true);
    setErr(null);
    try {
      await api.startRun(missionId);
      await reload();
    } catch (e) {
      setErr(String((e as Error).message ?? e));
    } finally {
      setBusy(false);
    }
  }

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-64" />
        <div className="grid gap-4 lg:grid-cols-3">
          <Skeleton className="h-96 lg:col-span-2" />
          <Skeleton className="h-96" />
        </div>
      </div>
    );
  }
  if (error || !data) return <ErrorNote message={`Could not load mission (${error ?? "not found"}).`} />;

  const { mission, runDetail } = data;

  return (
    <div>
      <PageHeader
        eyebrow={
          <Link href="/missions" className="flex items-center gap-1 text-xs text-muted hover:text-accent">
            <ArrowLeft size={13} /> Missions
          </Link>
        }
        title={
          <span className="flex items-center gap-3">
            {mission.title}
            <StatusBadge status={mission.status} />
          </span>
        }
        subtitle={mission.objective}
        actions={
          <Button variant="primary" onClick={startRun} loading={busy}>
            <Play size={15} /> Start Run
          </Button>
        }
      />

      {err && <div className="mb-4"><ErrorNote message={err} /></div>}

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <div className="flex items-center justify-between border-b border-line px-5 py-3.5">
            <div className="flex items-center gap-2 text-sm font-medium">
              <Rocket size={15} className="text-accent" /> Latest Run Timeline
            </div>
            {runDetail && <StatusBadge status={runDetail.status} />}
          </div>
          <div className="p-5">
            {runDetail ? <RunTimeline steps={runDetail.steps ?? []} /> : <div className="text-sm text-muted">No runs yet — start one.</div>}
          </div>
        </Card>

        <div className="space-y-4">
          <Card className="p-5">
            <SectionLabel>Mission</SectionLabel>
            <dl className="mt-3 space-y-3 text-sm">
              <InfoRow label="Status"><StatusBadge status={mission.status} /></InfoRow>
              <InfoRow label="Risk"><RiskBadge level={mission.risk_level} /></InfoRow>
              <InfoRow label="Priority"><span className="capitalize text-text">{mission.priority}</span></InfoRow>
              <InfoRow label="Created"><span className="text-muted">{fmtDate(mission.created_at)}</span></InfoRow>
            </dl>
            <div className="mt-4 space-y-2 border-t border-line-soft pt-4">
              {mission.source_idea_id && (
                <Link href={`/ideas/${mission.source_idea_id}`} className="flex items-center gap-2 text-xs text-muted hover:text-accent">
                  <Lightbulb size={13} /> Source idea <span className="mono ml-auto text-faint">{shortId(mission.source_idea_id)}</span>
                </Link>
              )}
              {mission.source_blueprint_id && (
                <div className="flex items-center gap-2 text-xs text-muted">
                  <FileText size={13} /> Blueprint <span className="mono ml-auto text-faint">{shortId(mission.source_blueprint_id)}</span>
                </div>
              )}
            </div>
          </Card>

          <Card>
            <div className="border-b border-line px-5 py-3">
              <SectionLabel>Runs ({mission.runs?.length ?? 0})</SectionLabel>
            </div>
            <div className="divide-line">
              {mission.runs?.map((r) => (
                <Link key={r.id} href={`/runs/${r.id}`} className="flex items-center gap-3 px-5 py-3 hover:bg-white/5">
                  <StatusBadge status={r.status} dot={false} />
                  <span className="mono text-xs text-faint">{shortId(r.id)}</span>
                  <span className="mono ml-auto text-[11px] text-muted">
                    {r.total_input_tokens + r.total_output_tokens} tok
                  </span>
                </Link>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}

function InfoRow({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="flex items-center justify-between">
      <dt className="text-muted">{label}</dt>
      <dd>{children}</dd>
    </div>
  );
}

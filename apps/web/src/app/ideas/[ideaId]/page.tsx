"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  Check,
  FileText,
  Layers,
  Rocket,
  Sparkles,
} from "lucide-react";

import { BestPartsPanel } from "@/components/ideas/BestPartsPanel";
import { BlueprintPanel } from "@/components/ideas/BlueprintPanel";
import { CouncilRoom } from "@/components/ideas/CouncilRoom";
import { PageHeader } from "@/components/layout/PageHeader";
import { Button, Card, ErrorNote, SectionLabel, Skeleton, StatusBadge } from "@/components/ui";
import { api } from "@/lib/api";
import { useApi } from "@/lib/useApi";
import { cx } from "@/lib/ui";

export default function IdeaDetailPage() {
  const { ideaId } = useParams<{ ideaId: string }>();
  const router = useRouter();
  const [busy, setBusy] = useState<string | null>(null);
  const [err, setErr] = useState<string | null>(null);

  const { data, error, loading, reload } = useApi(
    () =>
      Promise.all([
        api.getIdea(ideaId),
        api.getIdeaCouncil(ideaId),
        api.getIdeaBestParts(ideaId),
        api.getIdeaBlueprint(ideaId),
      ]),
    [ideaId],
  );

  const [idea, council, parts, blueprint] = data ?? [];
  const hasCouncil = !!council && council.contributions.length > 0;
  const hasParts = (parts?.length ?? 0) > 0;
  const hasBlueprint = !!blueprint;

  async function act(name: string, fn: () => Promise<unknown>) {
    setBusy(name);
    setErr(null);
    try {
      await fn();
      await reload();
    } catch (e) {
      setErr(String((e as Error).message ?? e));
    } finally {
      setBusy(null);
    }
  }

  async function promote() {
    setBusy("promote");
    setErr(null);
    try {
      const mission = await api.promoteToMission(ideaId);
      router.push(`/missions/${mission.id}`);
    } catch (e) {
      setErr(String((e as Error).message ?? e));
      setBusy(null);
    }
  }

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-20" />
        <div className="grid gap-4 lg:grid-cols-2">
          <Skeleton className="h-96" />
          <Skeleton className="h-96" />
        </div>
      </div>
    );
  }

  if (error || !idea) {
    return <ErrorNote message={`Could not load idea (${error ?? "not found"}).`} />;
  }

  return (
    <div>
      <PageHeader
        eyebrow={
          <Link href="/ideas" className="flex items-center gap-1 text-xs text-muted hover:text-accent">
            <ArrowLeft size={13} /> Forge
          </Link>
        }
        title={
          <span className="flex items-center gap-3">
            {idea.title}
            <StatusBadge status={idea.status} />
          </span>
        }
        subtitle={idea.description ?? undefined}
        actions={
          idea.status === "promoted_to_mission" ? (
            <Button variant="ghost" onClick={() => act("archive", () => api.archiveIdea(ideaId))} loading={busy === "archive"}>
              Archive
            </Button>
          ) : null
        }
      />

      {(err || undefined) && <div className="mb-4"><ErrorNote message={err!} /></div>}

      {/* Pipeline action rail */}
      <Card className="mb-4 p-4">
        <div className="flex flex-wrap items-center gap-2">
          <PipelineButton
            icon={<Sparkles size={15} />}
            label={hasCouncil ? "Re-run Council" : "Run Council"}
            done={hasCouncil}
            primary={!hasCouncil}
            loading={busy === "council"}
            onClick={() => act("council", () => api.runCouncil(ideaId))}
          />
          <Arrow />
          <PipelineButton
            icon={<Layers size={15} />}
            label="Extract Best Parts"
            done={hasParts}
            primary={hasCouncil && !hasParts}
            disabled={!hasCouncil}
            loading={busy === "parts"}
            onClick={() => act("parts", () => api.extractBestParts(ideaId))}
          />
          <Arrow />
          <PipelineButton
            icon={<FileText size={15} />}
            label="Generate Blueprint"
            done={hasBlueprint}
            primary={hasParts && !hasBlueprint}
            disabled={!hasParts}
            loading={busy === "blueprint"}
            onClick={() => act("blueprint", () => api.generateBlueprint(ideaId))}
          />
          <Arrow />
          <PipelineButton
            icon={<Rocket size={15} />}
            label="Promote to Mission"
            primary={hasBlueprint}
            disabled={!hasBlueprint}
            loading={busy === "promote"}
            onClick={promote}
          />
        </div>
      </Card>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <div className="space-y-4">
          <CouncilRoom run={council ?? null} running={busy === "council"} />
          {hasParts && <BestPartsPanel parts={parts!} />}
        </div>
        <div className="space-y-4">
          <SeedCard idea={idea} />
          {hasBlueprint && <BlueprintPanel blueprint={blueprint!} />}
        </div>
      </div>
    </div>
  );
}

function SeedCard({ idea }: { idea: { seed_prompt: string; tags: string[]; idea_score: number | null; risk_score: number | null; readiness_score: number | null } }) {
  return (
    <Card>
      <div className="border-b border-line px-5 py-3.5">
        <SectionLabel>Seed Idea</SectionLabel>
      </div>
      <div className="p-5">
        <p className="text-sm leading-relaxed text-text">{idea.seed_prompt}</p>
        {idea.tags.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1.5">
            {idea.tags.map((t) => (
              <span key={t} className="mono rounded-md border border-line bg-panel px-1.5 py-0.5 text-[10px] text-muted">
                {t}
              </span>
            ))}
          </div>
        )}
        <div className="mt-4 grid grid-cols-3 gap-3 border-t border-line-soft pt-4">
          <Score label="Idea Score" value={idea.idea_score} />
          <Score label="Risk" value={idea.risk_score} />
          <Score label="Readiness" value={idea.readiness_score} suffix={idea.readiness_score != null ? "%" : ""} />
        </div>
      </div>
    </Card>
  );
}

function Score({ label, value, suffix = "" }: { label: string; value: number | null; suffix?: string }) {
  return (
    <div>
      <div className="label">{label}</div>
      <div className="mono mt-1 text-lg font-semibold tabular-nums text-text">
        {value != null ? `${value}${suffix}` : "—"}
      </div>
    </div>
  );
}

function Arrow() {
  return <ArrowRight size={15} className="hidden shrink-0 text-faint sm:block" />;
}

function PipelineButton({
  icon,
  label,
  done,
  primary,
  disabled,
  loading,
  onClick,
}: {
  icon: React.ReactNode;
  label: string;
  done?: boolean;
  primary?: boolean;
  disabled?: boolean;
  loading?: boolean;
  onClick: () => void;
}) {
  return (
    <Button
      variant={primary ? "primary" : "secondary"}
      onClick={onClick}
      disabled={disabled}
      loading={loading}
      className={cx(done && !primary && "border-ok/30 text-ok")}
    >
      {done && !loading ? <Check size={15} /> : icon}
      {label}
    </Button>
  );
}

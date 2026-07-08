"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { ArrowLeft, Sparkles } from "lucide-react";

import { PageHeader } from "@/components/layout/PageHeader";
import { Button, Card, ErrorNote, SectionLabel } from "@/components/ui";
import { api } from "@/lib/api";
import { cx } from "@/lib/ui";

const OUTPUT_TYPES = ["idea", "blueprint", "app", "workflow", "report", "open-source project"];
const AUTONOMY = ["recommend only", "draft", "execute with approvals"];

export default function NewIdeaPage() {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [seedPrompt, setSeedPrompt] = useState("");
  const [description, setDescription] = useState("");
  const [tags, setTags] = useState("");
  const [outputType, setOutputType] = useState(OUTPUT_TYPES[0]);
  const [autonomy, setAutonomy] = useState(AUTONOMY[0]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const idea = await api.createIdea({
        title: title.trim(),
        seed_prompt: seedPrompt.trim(),
        description: description.trim() || undefined,
        tags: tags.split(",").map((t) => t.trim()).filter(Boolean),
        target_output_type: outputType,
        autonomy_preference: autonomy,
      });
      router.push(`/ideas/${idea.id}`);
    } catch (err) {
      setError(String((err as Error).message ?? err));
      setSubmitting(false);
    }
  }

  const valid = title.trim().length > 0 && seedPrompt.trim().length > 0;

  return (
    <div className="mx-auto max-w-2xl">
      <PageHeader
        eyebrow={
          <Link href="/ideas" className="flex items-center gap-1 text-xs text-muted hover:text-accent">
            <ArrowLeft size={13} /> Forge
          </Link>
        }
        title="New Idea"
        subtitle="Give the council something to work with. The seed prompt is what each seat reasons over."
      />

      <Card className="p-6">
        <form onSubmit={submit} className="space-y-5">
          <Field label="Title" required>
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Agentic release-notes generator"
              className={inputClass}
              autoFocus
            />
          </Field>

          <Field label="Seed prompt" required hint="The core idea, in your words.">
            <textarea
              value={seedPrompt}
              onChange={(e) => setSeedPrompt(e.target.value)}
              rows={4}
              placeholder="Describe the idea you want the council to develop…"
              className={cx(inputClass, "resize-y")}
            />
          </Field>

          <Field label="Description" hint="Optional extra context.">
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={2}
              className={cx(inputClass, "resize-y")}
            />
          </Field>

          <Field label="Tags" hint="Comma-separated.">
            <input
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              placeholder="agentic, open-source"
              className={inputClass}
            />
          </Field>

          <div className="grid gap-5 sm:grid-cols-2">
            <Field label="Target output">
              <select value={outputType} onChange={(e) => setOutputType(e.target.value)} className={inputClass}>
                {OUTPUT_TYPES.map((o) => (
                  <option key={o} value={o} className="bg-panel">
                    {o}
                  </option>
                ))}
              </select>
            </Field>
            <Field label="Autonomy preference">
              <select value={autonomy} onChange={(e) => setAutonomy(e.target.value)} className={inputClass}>
                {AUTONOMY.map((o) => (
                  <option key={o} value={o} className="bg-panel">
                    {o}
                  </option>
                ))}
              </select>
            </Field>
          </div>

          {error && <ErrorNote message={error} />}

          <div className="flex items-center justify-end gap-2 border-t border-line-soft pt-4">
            <Link href="/ideas">
              <Button type="button" variant="ghost">
                Cancel
              </Button>
            </Link>
            <Button type="submit" variant="primary" loading={submitting} disabled={!valid}>
              <Sparkles size={15} /> Create Idea
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
}

const inputClass =
  "w-full rounded-lg border border-line bg-bg-2 px-3 py-2 text-sm text-text placeholder:text-faint focus-ring transition focus:border-accent/50";

function Field({
  label,
  hint,
  required,
  children,
}: {
  label: string;
  hint?: string;
  required?: boolean;
  children: React.ReactNode;
}) {
  return (
    <label className="block">
      <div className="mb-1.5 flex items-baseline justify-between">
        <SectionLabel>
          {label}
          {required && <span className="ml-1 text-fail">*</span>}
        </SectionLabel>
        {hint && <span className="text-[11px] text-faint">{hint}</span>}
      </div>
      {children}
    </label>
  );
}

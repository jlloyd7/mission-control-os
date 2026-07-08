import type {
  Agent,
  Approval,
  AuditLog,
  BestPart,
  Blueprint,
  CouncilRun,
  CreateIdeaInput,
  Idea,
  Mission,
  MissionRun,
  RiskSummary,
  Tool,
} from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!res.ok) {
    let detail = "";
    try {
      const body = await res.json();
      detail = body.detail ?? JSON.stringify(body);
    } catch {
      detail = await res.text();
    }
    throw new Error(`${res.status} ${detail}`);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

const post = <T>(path: string, body?: unknown) =>
  request<T>(path, { method: "POST", body: body ? JSON.stringify(body) : undefined });

export const api = {
  base: API_BASE_URL,

  // Ideas
  listIdeas: () => request<Idea[]>("/ideas"),
  createIdea: (body: CreateIdeaInput) => post<Idea>("/ideas", body),
  getIdea: (id: string) => request<Idea>(`/ideas/${id}`),
  archiveIdea: (id: string) => request<void>(`/ideas/${id}`, { method: "DELETE" }),

  runCouncil: (id: string) => post<CouncilRun>(`/ideas/${id}/run-council`),
  extractBestParts: (id: string) => post<BestPart[]>(`/ideas/${id}/extract-best-parts`),
  generateBlueprint: (id: string) => post<Blueprint>(`/ideas/${id}/generate-blueprint`),
  promoteToMission: (id: string) => post<Mission>(`/ideas/${id}/promote-to-mission`),

  getIdeaCouncil: (id: string) => request<CouncilRun | null>(`/ideas/${id}/council`),
  getIdeaBestParts: (id: string) => request<BestPart[]>(`/ideas/${id}/best-parts`),
  getIdeaBlueprint: (id: string) => request<Blueprint | null>(`/ideas/${id}/blueprint`),

  // Missions & runs
  listMissions: () => request<Mission[]>("/missions"),
  getMission: (id: string) => request<Mission>(`/missions/${id}`),
  startRun: (id: string) => post<MissionRun>(`/missions/${id}/start-run`),
  getRun: (id: string) => request<MissionRun>(`/runs/${id}`),

  // Registry
  listAgents: () => request<Agent[]>("/agents"),
  listTools: () => request<Tool[]>("/tools"),

  // Approvals
  listApprovals: () => request<Approval[]>("/approvals"),
  approve: (id: string, reason?: string) =>
    post<Approval>(`/approvals/${id}/approve`, { reason }),
  reject: (id: string, reason?: string) =>
    post<Approval>(`/approvals/${id}/reject`, { reason }),

  // Governance
  auditLogs: () => request<AuditLog[]>("/governance/audit-logs"),
  riskSummary: () => request<RiskSummary>("/governance/risk-summary"),
};

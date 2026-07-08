// API response types (mirror apps/api schemas).

export type AgentKey = "george" | "cipher_fable" | "arty_codex";

export interface Idea {
  id: string;
  title: string;
  seed_prompt: string;
  description: string | null;
  status: string;
  tags: string[];
  idea_score: number | null;
  risk_score: number | null;
  readiness_score: number | null;
  created_at: string;
  updated_at: string;
}

export interface CreateIdeaInput {
  title: string;
  seed_prompt: string;
  description?: string;
  tags?: string[];
  target_output_type?: string;
  autonomy_preference?: string;
}

export interface ScoreBlock {
  user_value: number;
  strategic_value: number;
  originality: number;
  feasibility: number;
  revenue_potential: number;
  risk: number;
  build_effort: number;
}

export interface IdeaFragment {
  part_type: string;
  title: string;
  summary: string;
  why_it_matters: string;
  score: ScoreBlock;
  recommended_decision: string;
}

export interface CouncilProposal {
  agent_key: AgentKey;
  title: string;
  summary: string;
  assumptions: string[];
  proposal: string;
  best_features: IdeaFragment[];
  weak_points: string[];
  risks: string[];
  dependencies: string[];
  build_steps: string[];
  human_approval_needed: string[];
  confidence: number;
}

export interface CouncilContribution {
  id: string;
  council_run_id: string;
  agent_key: AgentKey;
  agent_name: string;
  provider: string;
  model_name: string;
  contribution_type: string;
  title: string | null;
  summary: string;
  content: CouncilProposal;
  confidence: number | null;
  created_at: string;
}

export interface CouncilRun {
  id: string;
  idea_id: string;
  status: string;
  mode: string;
  started_at: string | null;
  completed_at: string | null;
  error_message: string | null;
  created_at: string;
  contributions: CouncilContribution[];
}

export interface BestPart {
  id: string;
  idea_id: string;
  council_run_id: string | null;
  source_agent_key: AgentKey;
  part_type: string;
  title: string;
  summary: string;
  user_value: number | null;
  strategic_value: number | null;
  originality: number | null;
  feasibility: number | null;
  revenue_potential: number | null;
  risk: number | null;
  build_effort: number | null;
  weighted_score: number | null;
  decision: string;
  rationale: string | null;
  created_at: string;
}

export interface BlueprintFeature {
  name: string;
  description: string;
  priority: string;
  source_agent_keys: string[];
  acceptance_criteria: string[];
}

export interface Blueprint {
  id: string;
  idea_id: string;
  council_run_id: string | null;
  title: string;
  summary: string;
  product_brief: string;
  user_flow: string[];
  feature_list: BlueprintFeature[];
  technical_architecture: Record<string, unknown>;
  agent_roles: Record<string, string>;
  tool_requirements: string[];
  risk_controls: string[];
  sprint_plan: Array<Record<string, unknown>>;
  lineage: Array<Record<string, unknown>>;
  readiness_score: number | null;
  created_at: string;
  updated_at: string;
}

export interface Mission {
  id: string;
  source_idea_id: string | null;
  source_blueprint_id: string | null;
  title: string;
  objective: string;
  status: string;
  priority: string;
  owner_user_id: string | null;
  risk_level: string;
  created_at: string;
  updated_at: string;
  runs?: MissionRun[];
}

export interface MissionRun {
  id: string;
  mission_id: string;
  status: string;
  run_mode: string;
  started_at: string | null;
  completed_at: string | null;
  total_input_tokens: number;
  total_output_tokens: number;
  estimated_cost_usd: number;
  error_message: string | null;
  created_at: string;
  steps?: RunStep[];
}

export interface RunStep {
  id: string;
  run_id: string | null;
  council_run_id: string | null;
  step_index: number;
  step_type: string;
  agent_key: string | null;
  title: string;
  summary: string | null;
  input_payload: Record<string, unknown>;
  output_payload: Record<string, unknown>;
  status: string;
  started_at: string | null;
  completed_at: string | null;
  error_message: string | null;
  created_at: string;
}

export interface Agent {
  id: string;
  key: AgentKey;
  name: string;
  persona: string;
  provider: string;
  model_name: string;
  autonomy_level: string;
  risk_level: string;
  is_enabled: boolean;
  bbom: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface Tool {
  id: string;
  key: string;
  name: string;
  description: string;
  tool_type: string;
  can_read: boolean;
  can_write: boolean;
  can_delete: boolean;
  requires_approval: boolean;
  risk_level: string;
  is_enabled: boolean;
}

export interface Approval {
  id: string;
  mission_id: string | null;
  run_id: string | null;
  tool_id: string | null;
  requested_by_agent_key: string | null;
  title: string;
  description: string;
  action_payload: Record<string, unknown>;
  risk_level: string;
  status: string;
  decided_by_user_id: string | null;
  decision_reason: string | null;
  decided_at: string | null;
  created_at: string;
}

export interface AuditLog {
  id: string;
  actor_user_id: string | null;
  actor_agent_key: string | null;
  event_type: string;
  entity_type: string;
  entity_id: string | null;
  summary: string;
  payload: Record<string, unknown>;
  created_at: string;
}

export interface RiskSummary {
  tools_by_risk: Record<string, number>;
  pending_approvals: number;
  enabled_high_risk_tools: number;
  disabled_dangerous_tools: number;
}

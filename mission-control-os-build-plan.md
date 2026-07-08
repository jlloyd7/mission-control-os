# Mission Control OS — Detailed Frontend + Backend Build Plan

**Project codename:** Mission Control OS / MCOS  
**Primary product idea:** An open-source agentic mission-control platform where ideas become blueprints, blueprints become missions, and agents collaborate under human oversight.  
**Core council:**

| Seat | Persona | Engine / Provider | Primary responsibility |
|---|---|---|---|
| 1 | **George** | OpenAI / GPT-5.6 Sol or configured OpenAI model | Mission commander, architect, strategist, synthesis, final blueprint |
| 2 | **Fable / Cipher** | Anthropic / Claude Fable, Opus, or configured Anthropic model | Defensive systems reviewer, risk, security, assumptions, failure modes |
| 3 | **Arty** | GPT-5.6 Sol / Codex or configured coding model | Maker, UI/UX, prototype, code scaffold, visual/build concepts |

> Important implementation note: treat `George`, `Fable/Cipher`, and `Arty` as **logical seats**, not hardcoded model dependencies. The app should support model routing through environment variables and provider adapters.

---

## 0. What Opus should build first

The first skeleton should prove one full vertical slice:

```text
Create Idea
  → Run Council: George + Fable/Cipher + Arty
  → Extract Best Parts
  → Generate Blueprint
  → Promote Blueprint to Mission
  → View Mission Run Timeline
  → View Approval + Risk placeholders
```

The first skeleton does **not** need real external tool execution. It should use mock tools and mock agent responses by default, then make real OpenAI/Anthropic providers pluggable behind feature flags.

### P0 target for the initial build

Build this before anything else:

```text
1. Monorepo scaffold
2. Next.js frontend shell
3. FastAPI backend shell
4. Postgres schema + migrations
5. Mock agent council service
6. Ideas page
7. Idea detail page
8. Council run API
9. Best-parts extraction API
10. Blueprint generation API
11. Promote-to-mission API
12. Mission detail timeline UI
13. Docker Compose
14. README with setup commands
```

### Do not build yet

Leave these as interfaces/stubs for later:

```text
- Real browser automation
- Real Gmail/Slack/CRM actions
- Production deployments
- Arbitrary shell execution
- Paid tool actions
- Complex memory retrieval
- Multi-tenant billing
- Marketplace/plugin system
```

---

## 1. Product vision

Mission Control OS is a command center for agentic creation.

It should let a user:

1. Capture a raw idea.
2. Send the idea to a structured agent council.
3. Have George produce strategy and architecture.
4. Have Fable/Cipher challenge the idea, review risk, and harden it.
5. Have Arty turn the idea into design/build/prototype direction.
6. Extract the best parts from each contribution.
7. Synthesize a build-ready blueprint.
8. Promote the blueprint into an executable mission.
9. Track the mission through steps, approvals, tools, traces, and outputs.
10. Open-source the base platform so others can plug in their own models/tools.

The product is not just a chatbot. It is a **creation and governance control plane**.

---

## 2. Product modules

### 2.1 Forge / Ideas

Purpose: capture raw ideas and evolve them into structured blueprints.

Core features:

```text
- Create idea
- Edit idea
- Tag idea
- Score idea
- Run council
- Show George / Cipher / Arty proposals
- Extract best parts
- Generate blueprint
- Promote to mission
```

### 2.2 Council Room

Purpose: structured multi-agent collaboration.

Core features:

```text
- Three-seat council
- Independent agent proposals
- Cross-review option
- Best-parts extraction
- Unified synthesis
- Lineage: which idea fragment came from which agent
```

### 2.3 Mission Control

Purpose: track execution of blueprints as missions.

Core features:

```text
- Mission board
- Mission status
- Run timeline
- Step logs
- Tool calls
- Artifacts
- Human approvals
- Risk status
- Cost and token placeholder metrics
```

### 2.4 Agents

Purpose: manage agent seats, prompts, versions, model routing, and BBOM.

Core features:

```text
- Agent registry
- Agent version history
- System prompt editor later
- Model provider settings
- Role and policy card
- Behavioral Bill of Materials per agent
```

### 2.5 Tools

Purpose: show what agents can access.

Core features:

```text
- Tool registry
- Tool permissions
- Read/write capability
- Risk level
- Approval required flag
- Mock execution logs
- MCP-ready adapter interface
```

### 2.6 Approvals

Purpose: human approval center for risky actions.

Core features:

```text
- Pending approvals
- Approve / reject
- Approval reason
- Action preview
- Risk score
- Audit log
```

### 2.7 Governance

Purpose: safety, policy, BBOM, audit, and risk.

Core features:

```text
- RBAC roles
- Audit logs
- Risk scoring
- BBOM registry
- Memory write review
- Tool blast-radius view
- Agent autonomy level
```

### 2.8 Observability

Purpose: trace, debug, evaluate, and measure agent behavior.

Core features:

```text
- Run timeline
- Step-level traces
- Token/cost placeholders
- Latency placeholders
- Provider request/response metadata
- Langfuse integration later
```

---

## 3. High-level architecture

```mermaid
flowchart TD
  U[User] --> WEB[Next.js Web App]
  WEB --> API[FastAPI Control Plane API]
  API --> DB[(Postgres)]
  API --> REDIS[(Redis Queue / Cache)]
  API --> AGENT[Agent Orchestrator]
  AGENT --> OPENAI[OpenAI Provider Adapter]
  AGENT --> ANTHROPIC[Anthropic Provider Adapter]
  AGENT --> MOCK[Mock Provider Adapter]
  AGENT --> TOOLGW[Tool Gateway]
  TOOLGW --> MCP[MCP Servers later]
  TOOLGW --> INTERNAL[Internal Function Tools]
  API --> TRACE[Trace / Observability Adapter]
  TRACE --> LANGFUSE[Langfuse later]
```

### Recommended stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | Next.js App Router + TypeScript | Fast UI skeleton, open-source friendly |
| UI | Tailwind + shadcn/ui + lucide-react | Quick polished command-center interface |
| API | FastAPI + Python | Good fit for OpenAI/Anthropic agent SDKs and Pydantic schemas |
| ORM | SQLAlchemy 2 + Alembic | Strong Python backend migration path |
| DB | Postgres | Durable mission/agent/audit storage |
| Vector later | pgvector | Keep infra simple in the beginning |
| Queue | Redis + RQ/Celery/Arq later | Async mission execution |
| Auth P0 | Local dev user / simple JWT stub | Avoid auth complexity during skeleton |
| Auth P1 | Clerk/Auth0/WorkOS/Supabase Auth | Production-ready auth later |
| Observability P0 | Internal traces table | No external dependency required |
| Observability P1 | Langfuse/OpenTelemetry | Real LLM tracing/cost/latency |
| Tool protocol | Internal tool interface, MCP-ready | MCP can be added without changing UX |

---

## 4. Repository structure

```text
mission-control-os/
  README.md
  LICENSE
  SECURITY.md
  CONTRIBUTING.md
  .env.example
  docker-compose.yml
  package.json
  pnpm-workspace.yaml

  apps/
    web/
      package.json
      next.config.ts
      tsconfig.json
      src/
        app/
          layout.tsx
          page.tsx
          dashboard/page.tsx
          ideas/page.tsx
          ideas/new/page.tsx
          ideas/[ideaId]/page.tsx
          missions/page.tsx
          missions/[missionId]/page.tsx
          runs/[runId]/page.tsx
          agents/page.tsx
          agents/[agentId]/page.tsx
          tools/page.tsx
          approvals/page.tsx
          governance/page.tsx
          memory/page.tsx
          settings/page.tsx
        components/
          layout/
            AppShell.tsx
            Sidebar.tsx
            Topbar.tsx
            CommandBreadcrumbs.tsx
          ideas/
            IdeaCard.tsx
            IdeaForm.tsx
            CouncilRunPanel.tsx
            AgentProposalCard.tsx
            BestPartsPanel.tsx
            BlueprintPanel.tsx
          missions/
            MissionBoard.tsx
            MissionCard.tsx
            RunTimeline.tsx
            RunStepCard.tsx
          agents/
            AgentSeatCard.tsx
            AgentBBOMCard.tsx
          tools/
            ToolCard.tsx
            ToolRiskBadge.tsx
          approvals/
            ApprovalCard.tsx
          shared/
            StatusBadge.tsx
            RiskBadge.tsx
            EmptyState.tsx
            LoadingPanel.tsx
            JsonViewer.tsx
        lib/
          api.ts
          types.ts
          utils.ts
          mock-data.ts
        styles/
          globals.css

    api/
      pyproject.toml
      alembic.ini
      README.md
      app/
        main.py
        config.py
        db.py
        dependencies.py
        models/
          base.py
          organization.py
          user.py
          idea.py
          agent.py
          mission.py
          run.py
          tool.py
          approval.py
          memory.py
          audit.py
        schemas/
          common.py
          idea.py
          agent.py
          mission.py
          run.py
          tool.py
          approval.py
          council.py
          blueprint.py
        routers/
          health.py
          ideas.py
          council.py
          missions.py
          runs.py
          agents.py
          tools.py
          approvals.py
          governance.py
        services/
          agent_orchestrator.py
          council_service.py
          synthesis_service.py
          scoring_service.py
          mission_service.py
          risk_service.py
          audit_service.py
          trace_service.py
          approval_service.py
          tool_gateway.py
        providers/
          base.py
          mock_provider.py
          openai_provider.py
          anthropic_provider.py
        prompts/
          george.md
          cipher_fable.md
          arty.md
          synthesis.md
          best_parts.md
          blueprint.md
        migrations/
          versions/
        tests/
          test_health.py
          test_idea_flow.py
          test_scoring.py
          test_council_mock.py

  docs/
    architecture.md
    agent-roles.md
    api.md
    open-source-roadmap.md
    security-model.md
    prompt-library.md

  infra/
    docker/
    scripts/
      seed_dev.py
      reset_db.sh
```

---

## 5. Backend architecture

### 5.1 Backend responsibilities

The backend is the control plane. It owns:

```text
- User/org context
- Ideas and blueprints
- Council runs
- Mission creation
- Mission runs and steps
- Agent definitions
- Tool registry
- Approval decisions
- Audit logging
- Risk scoring
- Provider routing
- Trace capture
```

The frontend should not call OpenAI/Anthropic directly. All model calls go through the backend.

---

## 6. Database design

### 6.1 Core enums

Use enums or string columns with validation.

```text
idea_status:
  raw
  council_ready
  council_running
  council_complete
  best_parts_extracted
  blueprint_ready
  promoted_to_mission
  archived

mission_status:
  draft
  queued
  running
  blocked
  waiting_approval
  completed
  failed
  cancelled

run_status:
  queued
  running
  paused
  waiting_approval
  completed
  failed
  cancelled

step_type:
  user_input
  agent_thought_summary
  agent_proposal
  tool_call
  tool_result
  best_parts_extraction
  blueprint_generation
  approval_request
  approval_decision
  artifact_created
  error

approval_status:
  pending
  approved
  rejected
  expired
  cancelled

risk_level:
  low
  medium
  high
  critical

autonomy_level:
  recommend_only
  draft_only
  execute_readonly
  execute_low_risk
  approval_required
  disabled
```

### 6.2 Tables

#### organizations

```sql
create table organizations (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  slug text unique not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

#### users

```sql
create table users (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id),
  email text unique not null,
  display_name text,
  role text not null default 'owner',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

#### ideas

```sql
create table ideas (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id),
  created_by_user_id uuid references users(id),
  title text not null,
  seed_prompt text not null,
  description text,
  status text not null default 'raw',
  tags text[] not null default '{}',
  idea_score numeric,
  risk_score numeric,
  readiness_score numeric,
  metadata jsonb not null default '{}',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

#### agents

```sql
create table agents (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id),
  key text not null,
  name text not null,
  persona text not null,
  provider text not null,
  model_name text not null,
  autonomy_level text not null default 'recommend_only',
  risk_level text not null default 'medium',
  is_enabled boolean not null default true,
  metadata jsonb not null default '{}',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(organization_id, key)
);
```

#### agent_versions

```sql
create table agent_versions (
  id uuid primary key default gen_random_uuid(),
  agent_id uuid not null references agents(id),
  version integer not null,
  system_prompt text not null,
  output_schema jsonb not null default '{}',
  policy jsonb not null default '{}',
  bbom jsonb not null default '{}',
  created_by_user_id uuid references users(id),
  created_at timestamptz not null default now(),
  unique(agent_id, version)
);
```

#### council_runs

```sql
create table council_runs (
  id uuid primary key default gen_random_uuid(),
  idea_id uuid not null references ideas(id),
  organization_id uuid references organizations(id),
  status text not null default 'queued',
  mode text not null default 'triad',
  started_at timestamptz,
  completed_at timestamptz,
  error_message text,
  metadata jsonb not null default '{}',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

#### council_contributions

```sql
create table council_contributions (
  id uuid primary key default gen_random_uuid(),
  council_run_id uuid not null references council_runs(id),
  agent_key text not null,
  agent_name text not null,
  provider text not null,
  model_name text not null,
  contribution_type text not null,
  title text,
  summary text not null,
  content jsonb not null default '{}',
  confidence numeric,
  created_at timestamptz not null default now()
);
```

#### best_parts

```sql
create table best_parts (
  id uuid primary key default gen_random_uuid(),
  idea_id uuid not null references ideas(id),
  council_run_id uuid references council_runs(id),
  source_agent_key text not null,
  part_type text not null,
  title text not null,
  summary text not null,
  user_value integer,
  strategic_value integer,
  originality integer,
  feasibility integer,
  revenue_potential integer,
  risk integer,
  build_effort integer,
  weighted_score numeric,
  decision text not null default 'keep',
  rationale text,
  created_at timestamptz not null default now()
);
```

#### blueprints

```sql
create table blueprints (
  id uuid primary key default gen_random_uuid(),
  idea_id uuid not null references ideas(id),
  council_run_id uuid references council_runs(id),
  title text not null,
  summary text not null,
  product_brief text not null,
  user_flow jsonb not null default '{}',
  feature_list jsonb not null default '[]',
  technical_architecture jsonb not null default '{}',
  agent_roles jsonb not null default '{}',
  tool_requirements jsonb not null default '[]',
  risk_controls jsonb not null default '[]',
  sprint_plan jsonb not null default '[]',
  lineage jsonb not null default '[]',
  readiness_score numeric,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

#### missions

```sql
create table missions (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id),
  source_idea_id uuid references ideas(id),
  source_blueprint_id uuid references blueprints(id),
  title text not null,
  objective text not null,
  status text not null default 'draft',
  priority text not null default 'normal',
  owner_user_id uuid references users(id),
  risk_level text not null default 'medium',
  metadata jsonb not null default '{}',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

#### mission_runs

```sql
create table mission_runs (
  id uuid primary key default gen_random_uuid(),
  mission_id uuid not null references missions(id),
  organization_id uuid references organizations(id),
  status text not null default 'queued',
  run_mode text not null default 'mock',
  started_at timestamptz,
  completed_at timestamptz,
  total_input_tokens integer default 0,
  total_output_tokens integer default 0,
  estimated_cost_usd numeric default 0,
  error_message text,
  metadata jsonb not null default '{}',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

#### run_steps

```sql
create table run_steps (
  id uuid primary key default gen_random_uuid(),
  run_id uuid references mission_runs(id),
  council_run_id uuid references council_runs(id),
  organization_id uuid references organizations(id),
  step_index integer not null,
  step_type text not null,
  agent_key text,
  title text not null,
  summary text,
  input_payload jsonb not null default '{}',
  output_payload jsonb not null default '{}',
  status text not null default 'completed',
  started_at timestamptz default now(),
  completed_at timestamptz,
  error_message text,
  created_at timestamptz not null default now()
);
```

#### tools

```sql
create table tools (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id),
  key text not null,
  name text not null,
  description text not null,
  tool_type text not null default 'function',
  input_schema jsonb not null default '{}',
  output_schema jsonb not null default '{}',
  can_read boolean not null default true,
  can_write boolean not null default false,
  can_delete boolean not null default false,
  requires_approval boolean not null default true,
  risk_level text not null default 'medium',
  is_enabled boolean not null default false,
  metadata jsonb not null default '{}',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(organization_id, key)
);
```

#### approvals

```sql
create table approvals (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id),
  mission_id uuid references missions(id),
  run_id uuid references mission_runs(id),
  tool_id uuid references tools(id),
  requested_by_agent_key text,
  title text not null,
  description text not null,
  action_payload jsonb not null default '{}',
  risk_level text not null default 'medium',
  status text not null default 'pending',
  decided_by_user_id uuid references users(id),
  decision_reason text,
  decided_at timestamptz,
  created_at timestamptz not null default now()
);
```

#### artifacts

```sql
create table artifacts (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id),
  mission_id uuid references missions(id),
  run_id uuid references mission_runs(id),
  idea_id uuid references ideas(id),
  blueprint_id uuid references blueprints(id),
  artifact_type text not null,
  title text not null,
  content_text text,
  content_json jsonb not null default '{}',
  file_url text,
  created_by_agent_key text,
  created_at timestamptz not null default now()
);
```

#### audit_logs

```sql
create table audit_logs (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id),
  actor_user_id uuid references users(id),
  actor_agent_key text,
  event_type text not null,
  entity_type text not null,
  entity_id uuid,
  summary text not null,
  payload jsonb not null default '{}',
  created_at timestamptz not null default now()
);
```

---

## 7. API routes

### Health

```text
GET /health
GET /version
```

### Ideas

```text
GET    /ideas
POST   /ideas
GET    /ideas/{idea_id}
PATCH  /ideas/{idea_id}
DELETE /ideas/{idea_id}                 # soft archive only
POST   /ideas/{idea_id}/run-council
POST   /ideas/{idea_id}/extract-best-parts
POST   /ideas/{idea_id}/generate-blueprint
POST   /ideas/{idea_id}/promote-to-mission
```

### Council

```text
GET    /council-runs/{council_run_id}
GET    /council-runs/{council_run_id}/contributions
GET    /council-runs/{council_run_id}/steps
POST   /council-runs/{council_run_id}/rerun-agent/{agent_key}
POST   /council-runs/{council_run_id}/cross-review       # P1
```

### Blueprints

```text
GET    /blueprints/{blueprint_id}
PATCH  /blueprints/{blueprint_id}
POST   /blueprints/{blueprint_id}/promote-to-mission
```

### Missions

```text
GET    /missions
POST   /missions
GET    /missions/{mission_id}
PATCH  /missions/{mission_id}
POST   /missions/{mission_id}/start-run
POST   /missions/{mission_id}/cancel
```

### Runs

```text
GET    /runs/{run_id}
GET    /runs/{run_id}/steps
GET    /runs/{run_id}/events             # P1 SSE
POST   /runs/{run_id}/pause
POST   /runs/{run_id}/resume
POST   /runs/{run_id}/cancel
```

### Agents

```text
GET    /agents
POST   /agents
GET    /agents/{agent_id}
PATCH  /agents/{agent_id}
GET    /agents/{agent_id}/versions
POST   /agents/{agent_id}/versions
GET    /agents/{agent_id}/bbom
```

### Tools

```text
GET    /tools
POST   /tools
GET    /tools/{tool_id}
PATCH  /tools/{tool_id}
POST   /tools/{tool_id}/test             # mock only in P0
GET    /tools/{tool_id}/blast-radius
```

### Approvals

```text
GET    /approvals
GET    /approvals/{approval_id}
POST   /approvals/{approval_id}/approve
POST   /approvals/{approval_id}/reject
```

### Governance

```text
GET    /governance/audit-logs
GET    /governance/risk-summary
GET    /governance/bbom
GET    /governance/policies
```

---

## 8. Pydantic schemas

### 8.1 Council proposal schema

```python
from pydantic import BaseModel, Field
from typing import Literal

AgentKey = Literal["george", "cipher_fable", "arty_codex"]

class ScoreBlock(BaseModel):
    user_value: int = Field(ge=1, le=10)
    strategic_value: int = Field(ge=1, le=10)
    originality: int = Field(ge=1, le=10)
    feasibility: int = Field(ge=1, le=10)
    revenue_potential: int = Field(ge=1, le=10)
    risk: int = Field(ge=1, le=10)
    build_effort: int = Field(ge=1, le=10)

class IdeaFragment(BaseModel):
    part_type: Literal[
        "feature",
        "ux",
        "architecture",
        "automation",
        "security",
        "business",
        "launch",
        "risk",
        "open_source"
    ]
    title: str
    summary: str
    why_it_matters: str
    score: ScoreBlock
    recommended_decision: Literal["keep", "modify", "reject", "needs_evidence", "needs_human_approval"]

class CouncilProposal(BaseModel):
    agent_key: AgentKey
    title: str
    summary: str
    assumptions: list[str]
    proposal: str
    best_features: list[IdeaFragment]
    weak_points: list[str]
    risks: list[str]
    dependencies: list[str]
    build_steps: list[str]
    human_approval_needed: list[str]
    confidence: float = Field(ge=0, le=1)
```

### 8.2 Best-parts schema

```python
class BestPartDecision(BaseModel):
    source_agent_key: AgentKey
    part_type: str
    title: str
    summary: str
    decision: Literal["keep", "modify", "reject", "needs_evidence", "needs_human_approval"]
    rationale: str
    weighted_score: float
    merged_into_blueprint_section: str | None = None
```

### 8.3 Blueprint schema

```python
class BlueprintFeature(BaseModel):
    name: str
    description: str
    priority: Literal["P0", "P1", "P2", "Future"]
    source_agent_keys: list[AgentKey]
    acceptance_criteria: list[str]

class Blueprint(BaseModel):
    title: str
    summary: str
    product_brief: str
    target_user: str
    problem_statement: str
    success_metrics: list[str]
    feature_list: list[BlueprintFeature]
    user_flow: list[str]
    technical_architecture: dict
    data_model_notes: list[str]
    api_notes: list[str]
    agent_roles: dict
    tool_requirements: list[str]
    risk_controls: list[str]
    approval_gates: list[str]
    sprint_plan: list[dict]
    lineage: list[dict]
    open_questions: list[str]
    readiness_score: float
```

---

## 9. Agent provider interface

### 9.1 Base provider

Create `apps/api/app/providers/base.py`:

```python
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Any

class ModelMessage(BaseModel):
    role: str
    content: str

class ModelRequest(BaseModel):
    model: str
    system_prompt: str
    messages: list[ModelMessage]
    response_schema: dict[str, Any] | None = None
    temperature: float = 0.2
    max_tokens: int | None = None
    metadata: dict[str, Any] = {}

class ModelUsage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost_usd: float = 0.0

class ModelResponse(BaseModel):
    content_text: str
    content_json: dict[str, Any] | None = None
    usage: ModelUsage = ModelUsage()
    raw: dict[str, Any] = {}

class ModelProvider(ABC):
    @abstractmethod
    async def complete(self, request: ModelRequest) -> ModelResponse:
        raise NotImplementedError
```

### 9.2 Mock provider

P0 must work without API keys.

```python
class MockProvider(ModelProvider):
    async def complete(self, request: ModelRequest) -> ModelResponse:
        agent_key = request.metadata.get("agent_key", "unknown")
        # Return deterministic structured fake output based on agent_key.
        # This lets frontend and database flow be built before real model calls.
```

### 9.3 OpenAI provider

P1 integration.

```python
class OpenAIProvider(ModelProvider):
    async def complete(self, request: ModelRequest) -> ModelResponse:
        # Use OpenAI client / Agents SDK later.
        # For P1, simple structured Responses API or Agents SDK wrapper is enough.
```

### 9.4 Anthropic provider

P1 integration.

```python
class AnthropicProvider(ModelProvider):
    async def complete(self, request: ModelRequest) -> ModelResponse:
        # Use Anthropic Messages API or Claude Agent SDK wrapper.
        # Keep tool execution disabled until approval/tool gateway is ready.
```

---

## 10. Environment variables

Create `.env.example`:

```bash
# App
APP_ENV=development
APP_NAME=Mission Control OS
APP_BASE_URL=http://localhost:3000
API_BASE_URL=http://localhost:8000

# Database
DATABASE_URL=postgresql+psycopg://mcos:mcos@localhost:5432/mcos
POSTGRES_USER=mcos
POSTGRES_PASSWORD=mcos
POSTGRES_DB=mcos

# Redis
REDIS_URL=redis://localhost:6379/0

# Auth P0
DEV_AUTH_ENABLED=true
DEV_USER_EMAIL=george@example.local
DEV_ORG_NAME=Mission Control Dev

# Models
ENABLE_REAL_MODELS=false
DEFAULT_MODEL_PROVIDER=mock
GEORGE_PROVIDER=openai
GEORGE_MODEL=gpt-5.6-sol
CIPHER_PROVIDER=anthropic
CIPHER_MODEL=claude-fable-5
ARTY_PROVIDER=openai
ARTY_MODEL=gpt-5.6-sol-codex

# API keys - do not commit real values
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# Observability P1
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_HOST=http://localhost:3001

# Security
SECRET_KEY=change-me-in-dev
CORS_ORIGINS=http://localhost:3000
```

---

## 11. Docker Compose

Create `docker-compose.yml`:

```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: mcos
      POSTGRES_PASSWORD: mcos
      POSTGRES_DB: mcos
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

Optional P1 services:

```text
- langfuse
- minio
- qdrant
- temporal
```

Do not add them to P0 unless the skeleton is already working.

---

## 12. Backend service flow

### 12.1 Create idea

```text
POST /ideas
  → validate title + seed_prompt
  → create ideas row
  → audit log: idea.created
  → return idea
```

### 12.2 Run council

```text
POST /ideas/{idea_id}/run-council
  → load idea
  → create council_runs row status=running
  → create run_step: council started
  → run George proposal
  → save George contribution
  → run Fable/Cipher proposal
  → save Fable/Cipher contribution
  → run Arty proposal
  → save Arty contribution
  → mark council run complete
  → update idea.status=council_complete
  → audit log: council.completed
  → return council run with contributions
```

P0 can run synchronously. P1 should move to a queue worker.

### 12.3 Extract best parts

```text
POST /ideas/{idea_id}/extract-best-parts
  → load latest council run
  → collect contributions
  → call synthesis service or mock extractor
  → score each fragment
  → save best_parts rows
  → update idea.status=best_parts_extracted
  → return best parts
```

### 12.4 Generate blueprint

```text
POST /ideas/{idea_id}/generate-blueprint
  → load idea
  → load best parts
  → call blueprint synthesis
  → save blueprints row
  → create artifact: blueprint
  → update idea.status=blueprint_ready
  → return blueprint
```

### 12.5 Promote to mission

```text
POST /ideas/{idea_id}/promote-to-mission
  → load latest blueprint
  → create mission row
  → create initial mission_run or leave as draft
  → update idea.status=promoted_to_mission
  → audit log: mission.created_from_blueprint
  → return mission
```

---

## 13. Scoring logic

Create `scoring_service.py`:

```python
def weighted_part_score(
    user_value: int,
    strategic_value: int,
    originality: int,
    feasibility: int,
    revenue_potential: int,
    risk: int,
    build_effort: int,
) -> float:
    return round(
        (user_value * 1.5)
        + (strategic_value * 1.3)
        + (originality * 1.0)
        + (feasibility * 1.2)
        + (revenue_potential * 0.8)
        - (risk * 1.2)
        - (build_effort * 0.8),
        2,
    )
```

Idea score:

```text
idea_score = average weighted score of kept/modified fragments
```

Risk score:

```text
risk_score = average risk of kept/modified fragments + tool risk modifiers
```

Readiness score:

```text
readiness_score =
  blueprint_completeness
  + acceptance_criteria_presence
  + risk_controls_presence
  + tool_requirements_defined
  + owner_defined
  - open_questions_penalty
```

---

## 14. Prompt pack

Store prompts as Markdown files in `apps/api/app/prompts`.

### 14.1 George prompt

```md
# George — Mission Commander

You are George, the mission commander, architect, and final synthesizer for Mission Control OS.

Your job:
- Turn rough ideas into clear mission strategy.
- Define the opportunity, objective, architecture, and execution path.
- Identify the highest-leverage version of the idea.
- Keep the plan practical, buildable, and staged.
- Avoid vague inspiration. Produce operational structure.

You must output structured JSON matching the CouncilProposal schema.

Focus areas:
- Product strategy
- System architecture
- Mission design
- Execution roadmap
- Tradeoffs
- Best-parts synthesis potential
- Human approval checkpoints

Do not execute external actions. Do not claim work has been done unless it is represented in the current run data.
```

### 14.2 Fable/Cipher prompt

```md
# Fable/Cipher — Sentinel

You are Fable/Cipher, the defensive systems reviewer and adversarial thinking seat.

Your job:
- Challenge assumptions.
- Find risks, failure modes, security issues, and governance gaps.
- Improve the idea by making it safer, stronger, and more resilient.
- Identify tool permissions, memory risks, prompt-injection risks, data exposure, and approval gates.
- Recommend safer alternatives, not just objections.

You must output structured JSON matching the CouncilProposal schema.

Focus areas:
- Security
- Tool blast radius
- Human-in-the-loop controls
- Memory poisoning
- Prompt injection
- Unauthorized external actions
- Reliability
- Rollback plans
- Open-source safety

You are defensive only. Do not provide offensive security instructions or exploitation steps. Do not execute external actions.
```

### 14.3 Arty prompt

```md
# Arty — Maker

You are Arty, the maker, designer, and prototype builder.

Your job:
- Turn concepts into interfaces, components, flows, and buildable prototypes.
- Suggest UI/UX structure, visual hierarchy, frontend components, and code scaffold direction.
- Find the simplest useful first version.
- Make the product feel powerful but usable.

You must output structured JSON matching the CouncilProposal schema.

Focus areas:
- User experience
- Visual interface
- Frontend layout
- Components
- Product feel
- Prototype path
- Build tasks
- Open-source polish

Do not execute external actions. Do not claim files were created unless the build system created them.
```

### 14.4 Best-parts extraction prompt

```md
# Best Parts Extractor

You receive:
- Original seed idea
- George proposal
- Fable/Cipher proposal
- Arty proposal

Your job:
- Break each proposal into reusable idea fragments.
- Score each fragment.
- Decide keep, modify, reject, needs evidence, or needs human approval.
- Preserve lineage: every kept idea must cite the source agent.
- Do not blend everything blindly. Keep only the strongest compatible parts.

Output structured JSON matching the BestPartDecision list schema.
```

### 14.5 Blueprint synthesis prompt

```md
# Blueprint Synthesizer

You receive:
- Original idea
- Council contributions
- Best parts
- Rejected parts
- Risk notes

Your job:
- Create one build-ready blueprint.
- Make it specific enough to promote into a mission.
- Include product brief, features, user flow, architecture, agent roles, tool requirements, risk controls, approval gates, sprint plan, and lineage.
- Highlight open questions clearly.
- Keep the first build small enough to ship.

Output structured JSON matching the Blueprint schema.
```

---

## 15. Frontend design plan

### 15.1 Visual direction

Theme: command center / creation lab.

Style:

```text
- Dark base background
- Card panels
- Status lights
- Agent seat cards
- Timeline rails
- Subtle grid or console aesthetic
- Clear action buttons
- Avoid sci-fi clutter that hurts usability
```

Suggested nav labels:

```text
Dashboard
Forge
Missions
Approvals
Agents
Tools
Governance
Memory
Analytics
Settings
```

### 15.2 App shell

`AppShell.tsx` should include:

```text
- Sidebar navigation
- Topbar with environment badge
- Current org/user placeholder
- Command/search button placeholder
- Main content area
```

### 15.3 Dashboard page

Route: `/dashboard`

Panels:

```text
- Active missions
- Ideas ready for council
- Pending approvals
- Agent council health
- Recent run timeline
- Risk summary
```

P0 can use API data if available, otherwise mock empty state.

### 15.4 Ideas list page

Route: `/ideas`

Features:

```text
- Create idea button
- Idea cards
- Filter by status
- Filter by tag
- Sort by updated, readiness, risk
```

Idea card fields:

```text
- Title
- Seed summary
- Status
- Idea score
- Risk score
- Readiness score
- Last council run status
- Primary action: Open
```

### 15.5 New idea page

Route: `/ideas/new`

Fields:

```text
- Title
- Seed prompt
- Description
- Tags
- Target output type: idea / blueprint / app / workflow / report / open-source project
- Autonomy preference: recommend only / draft / execute with approvals
```

On submit:

```text
POST /ideas
redirect to /ideas/{ideaId}
```

### 15.6 Idea detail page

Route: `/ideas/[ideaId]`

Layout:

```text
Header:
  title, status, scores, actions

Left column:
  Seed idea
  Creation Quest answers later
  Best Parts
  Blueprint

Right column:
  Council Room
  Risk Panel
  Lineage Panel
```

Action buttons:

```text
Run Council
Extract Best Parts
Generate Blueprint
Promote to Mission
Archive
```

### 15.7 Council Room component

Show three cards:

```text
George — Commander
Fable/Cipher — Sentinel
Arty — Maker
```

Each card shows:

```text
- Status: waiting / running / complete / failed
- Summary
- Best features count
- Risks count
- Confidence
- Expand details
```

### 15.8 Best Parts panel

Show fragments grouped by decision:

```text
Keep
Modify
Needs Human Approval
Needs Evidence
Reject
```

Each fragment shows:

```text
- Source agent
- Part type
- Title
- Summary
- Score
- Decision
- Rationale
```

### 15.9 Blueprint panel

Show:

```text
- Summary
- Product brief
- Feature list by priority
- User flow
- Technical architecture
- Risk controls
- Sprint plan
- Lineage
```

### 15.10 Missions list page

Route: `/missions`

Board columns:

```text
Draft
Queued
Running
Waiting Approval
Completed
Failed
```

### 15.11 Mission detail page

Route: `/missions/[missionId]`

Panels:

```text
- Mission objective
- Current status
- Start run button
- Latest run timeline
- Related idea/blueprint
- Approvals
- Artifacts
```

### 15.12 Run detail page

Route: `/runs/[runId]`

Show:

```text
- Step timeline
- Agent outputs
- Tool calls
- Approval events
- Artifacts
- Errors
- Token/cost placeholders
```

### 15.13 Agents page

Route: `/agents`

Show:

```text
George Prime
Cipher Fable
Arty Codex
```

Each card:

```text
- Provider
- Model
- Persona
- Autonomy level
- Risk level
- Enabled
- BBOM summary
```

### 15.14 Tools page

Route: `/tools`

Show:

```text
- Mock tools
- Tool key/name
- Read/write/delete flags
- Requires approval
- Risk level
- Enabled
- Blast radius
```

Seed mock tools:

```text
- knowledge_search: read-only, low risk
- file_reader: read-only, medium risk
- blueprint_writer: internal write, low risk
- code_scaffold: local artifact write, medium risk
- deploy_app: external side effect, critical risk, disabled
- send_email: external side effect, high risk, disabled
```

### 15.15 Approvals page

Route: `/approvals`

Show:

```text
- Pending approvals
- Approved/rejected history
- Risk level
- Action preview
- Approve/reject buttons
```

P0 can seed sample approvals. P1 can generate approvals from tool calls.

---

## 16. Frontend API client

Create `apps/web/src/lib/api.ts`:

```ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

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
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }

  return res.json() as Promise<T>;
}

export const api = {
  listIdeas: () => request<Idea[]>("/ideas"),
  createIdea: (body: CreateIdeaInput) =>
    request<Idea>("/ideas", { method: "POST", body: JSON.stringify(body) }),
  getIdea: (id: string) => request<IdeaDetail>(`/ideas/${id}`),
  runCouncil: (id: string) =>
    request<CouncilRun>(`/ideas/${id}/run-council`, { method: "POST" }),
  extractBestParts: (id: string) =>
    request<BestPart[]>(`/ideas/${id}/extract-best-parts`, { method: "POST" }),
  generateBlueprint: (id: string) =>
    request<Blueprint>(`/ideas/${id}/generate-blueprint`, { method: "POST" }),
  promoteToMission: (id: string) =>
    request<Mission>(`/ideas/${id}/promote-to-mission`, { method: "POST" }),
};
```

Use TanStack Query in P1. For P0, simple `useEffect` + state is acceptable.

---

## 17. Mission lifecycle

```mermaid
stateDiagram-v2
  [*] --> RawIdea
  RawIdea --> CouncilReady
  CouncilReady --> CouncilRunning
  CouncilRunning --> CouncilComplete
  CouncilComplete --> BestPartsExtracted
  BestPartsExtracted --> BlueprintReady
  BlueprintReady --> MissionDraft
  MissionDraft --> MissionQueued
  MissionQueued --> MissionRunning
  MissionRunning --> WaitingApproval
  WaitingApproval --> MissionRunning
  WaitingApproval --> MissionCancelled
  MissionRunning --> MissionCompleted
  MissionRunning --> MissionFailed
```

---

## 18. Tool gateway design

### 18.1 Tool object

Every tool must define:

```text
key
name
description
input_schema
output_schema
can_read
can_write
can_delete
requires_approval
risk_level
timeout_seconds
allowed_agent_keys
```

### 18.2 Tool execution rules

P0:

```text
- No real external tool execution
- Mock results only
- Tool call rows can be created as simulated events
```

P1:

```text
- Read-only internal tools allowed
- Tool gateway checks permissions
- Tool gateway checks approval policy
- Tool gateway writes audit log
```

P2:

```text
- MCP server support
- Tool credentials stored securely
- Per-tool approval gates
- Rollback plan field
```

### 18.3 Approval gate rules

Require approval when:

```text
- Tool can write externally
- Tool can delete
- Tool can send communication
- Tool can spend money
- Tool can deploy
- Tool can access secrets
- Tool has high/critical risk
- Agent requests memory write containing sensitive data
```

---

## 19. Behavioral Bill of Materials

Each agent should have a BBOM card.

### 19.1 George BBOM

```json
{
  "agent_key": "george",
  "can_do": [
    "Create mission plans",
    "Synthesize blueprints",
    "Assign tasks to council seats",
    "Generate architecture recommendations",
    "Recommend approval gates"
  ],
  "cannot_do_without_approval": [
    "Send external messages",
    "Modify production data",
    "Deploy builds",
    "Spend money",
    "Delete files"
  ],
  "default_autonomy": "recommend_only",
  "risk_level": "medium"
}
```

### 19.2 Fable/Cipher BBOM

```json
{
  "agent_key": "cipher_fable",
  "can_do": [
    "Review risks",
    "Challenge assumptions",
    "Inspect tool permissions",
    "Generate defensive threat models",
    "Review build plans",
    "Recommend rollback plans"
  ],
  "cannot_do": [
    "Execute external actions",
    "Change permissions directly",
    "Override human approval",
    "Perform offensive exploitation"
  ],
  "default_autonomy": "recommend_only",
  "risk_level": "medium"
}
```

### 19.3 Arty BBOM

```json
{
  "agent_key": "arty_codex",
  "can_do": [
    "Generate UI concepts",
    "Scaffold code",
    "Create prototype plans",
    "Suggest components",
    "Draft build artifacts"
  ],
  "cannot_do_without_approval": [
    "Merge code",
    "Deploy",
    "Access secrets",
    "Modify live customer data",
    "Run arbitrary shell commands"
  ],
  "default_autonomy": "draft_only",
  "risk_level": "medium"
}
```

---

## 20. Security model

### 20.1 Core safety principles

```text
1. Default to read-only.
2. Default to mock tools in development.
3. Every side effect must be auditable.
4. High-risk actions require human approval.
5. Agents never receive secrets directly.
6. Tool access is allowlisted per agent.
7. Memory writes can be reviewed.
8. Prompt-injection warnings are surfaced in the run timeline.
9. Dangerous tools are disabled by default.
10. Open-source build must be safe out of the box.
```

### 20.2 RBAC roles

```text
owner:
  full access

admin:
  manage agents, tools, missions, approvals

builder:
  create ideas, run council, create missions, view traces

reviewer:
  view missions, approve/reject assigned approvals

viewer:
  read-only
```

P0 can stub this. P1 should enforce it.

### 20.3 Prompt-injection mitigations

```text
- Keep system prompts server-side.
- Never allow retrieved content to override system/tool policy.
- Mark external content as untrusted.
- Use tool allowlists.
- Use approval gates before side effects.
- Keep memory writes as structured pending records.
- Show suspicious instructions in risk panel.
```

### 20.4 Secret handling

```text
- Never log API keys.
- Never show secrets in traces.
- Use env vars locally.
- Use secret manager in production.
- Redact provider request headers.
- Redact tool credentials.
```

---

## 21. Observability plan

### P0 internal traces

Use `run_steps` and `audit_logs`.

Capture:

```text
- agent key
- model provider
- model name
- input summary
- output summary
- status
- token placeholders
- latency placeholders
- errors
```

### P1 Langfuse / OpenTelemetry

Add tracing adapter:

```python
class TraceService:
    async def start_trace(...): ...
    async def add_observation(...): ...
    async def end_trace(...): ...
```

Should support:

```text
- internal DB trace
- Langfuse trace
- OpenTelemetry trace
```

---

## 22. Seed data

Create `scripts/seed_dev.py` to seed:

```text
Organization:
  Mission Control Dev

User:
  George Dev <george@example.local>

Agents:
  george
  cipher_fable
  arty_codex

Tools:
  knowledge_search
  file_reader
  blueprint_writer
  code_scaffold
  deploy_app disabled
  send_email disabled

Sample idea:
  Build an agentic OS mission-control platform with an Ideas Forge and Council Room.
```

---

## 23. Initial mock council outputs

Use deterministic mock outputs so the UI looks alive.

### George mock summary

```text
Build a creation-to-execution control plane. Start with Ideas Forge, Council Room, Best Parts Extractor, Blueprints, and Mission Control. Use a monorepo, API control plane, Postgres state, and provider adapters.
```

### Fable/Cipher mock summary

```text
The core risks are tool misuse, excessive agency, memory poisoning, prompt injection, and unapproved external actions. Default to mock/read-only tools, BBOM cards, approval gates, audit logs, and risk scoring.
```

### Arty mock summary

```text
Make the product feel like a command center. Use a dark app shell, agent seat cards, idea cards, best-parts fragments, mission timelines, and a clear Create from Best Parts flow.
```

---

## 24. Open-source plan

### Recommended license

Use **Apache-2.0** if you want a permissive open-source license with explicit patent protections. Use **MIT** if you want maximum simplicity.

Recommendation:

```text
Apache-2.0
```

### Required repo files

```text
README.md
LICENSE
SECURITY.md
CONTRIBUTING.md
CODE_OF_CONDUCT.md
.env.example
```

### README sections

```text
- What is Mission Control OS?
- Why it exists
- Screenshots/GIF later
- Core concepts
- Architecture
- Quickstart
- Environment variables
- Running locally
- Mock model mode
- Real provider mode
- Security model
- Roadmap
- Contributing
- License
```

### Security disclaimer

Include:

```text
Mission Control OS is an experimental agentic workflow platform. It ships with mock/read-only defaults. Do not enable write tools, deploy tools, shell tools, customer data access, or external communication tools without reviewing and configuring approval gates, audit logging, RBAC, and secret management.
```

---

## 25. Build phases

### Phase 0 — Repo bootstrap

Deliverables:

```text
- Monorepo structure
- Docker Compose for Postgres/Redis
- Next.js app boots
- FastAPI app boots
- Health check works
- README quickstart
```

Acceptance criteria:

```text
- `docker compose up -d` starts Postgres/Redis
- API health returns OK
- Web app loads dashboard shell
```

### Phase 1 — Database + seed

Deliverables:

```text
- SQLAlchemy models
- Alembic migrations
- Dev seed script
- Agents/tools/sample idea seeded
```

Acceptance criteria:

```text
- DB migrates cleanly
- Seed script can be rerun safely
- GET /agents returns three agent seats
- GET /tools returns mock tools
```

### Phase 2 — Ideas Forge

Deliverables:

```text
- Create idea API
- List ideas API
- Idea detail API
- Ideas frontend pages
```

Acceptance criteria:

```text
- User can create an idea from UI
- User is redirected to idea detail
- Idea persists in Postgres
```

### Phase 3 — Council Room mock execution

Deliverables:

```text
- Council run API
- Mock provider
- Council contributions table
- Council Room UI cards
```

Acceptance criteria:

```text
- User clicks Run Council
- George/Fable/Arty cards populate
- Council run is saved
- Status updates to council_complete
```

### Phase 4 — Best Parts + Blueprint

Deliverables:

```text
- Best-parts extraction API
- Best-parts UI
- Blueprint generation API
- Blueprint UI
```

Acceptance criteria:

```text
- User clicks Extract Best Parts
- Fragments appear grouped by decision
- User clicks Generate Blueprint
- Blueprint appears with features, architecture, risks, sprint plan, lineage
```

### Phase 5 — Promote to Mission

Deliverables:

```text
- Promote-to-mission API
- Mission table integration
- Mission detail page
- Run timeline component
```

Acceptance criteria:

```text
- User promotes blueprint to mission
- Mission is created
- Mission detail links back to idea/blueprint
- Timeline shows creation events
```

### Phase 6 — Approval Center skeleton

Deliverables:

```text
- Approvals table/API
- Approval UI
- Sample pending approval
- Tool risk badges
```

Acceptance criteria:

```text
- Pending approvals display
- User can approve/reject mock approval
- Audit log records decision
```

### Phase 7 — Provider adapters

Deliverables:

```text
- OpenAI provider adapter
- Anthropic provider adapter
- Env-based model routing
- Feature flag ENABLE_REAL_MODELS
- Response parsing and validation
```

Acceptance criteria:

```text
- App works in mock mode without keys
- App can call real providers when keys and flag are set
- Invalid model output is caught and surfaced
```

### Phase 8 — Observability

Deliverables:

```text
- Trace service
- Run step logging everywhere
- Token/cost/latency fields
- Langfuse adapter optional
```

Acceptance criteria:

```text
- Every council run produces trace-like steps
- Every provider call has a step record
- Errors are visible in UI
```

### Phase 9 — MCP/tool gateway foundation

Deliverables:

```text
- Tool gateway interface
- Mock tool execution
- Permission checks
- Approval-required path
- MCP adapter placeholder
```

Acceptance criteria:

```text
- Tool cannot run if disabled
- High-risk/write tool creates approval request
- Tool result creates run step
```

### Phase 10 — Open-source polish

Deliverables:

```text
- Screenshots/GIF placeholders
- Security doc
- Contributing guide
- Issue templates
- Roadmap
- Good README
```

Acceptance criteria:

```text
- New developer can run locally from README
- No secrets committed
- Mock mode demonstrates the full vertical slice
```

---

## 26. Commands for Opus / Claude Code

### 26.1 Initial repo commands

```bash
mkdir mission-control-os
cd mission-control-os

git init
pnpm init
pnpm add -D turbo typescript prettier eslint
mkdir -p apps docs infra scripts packages
```

Better with pnpm workspace:

```bash
cat > pnpm-workspace.yaml <<'EOF'
packages:
  - "apps/*"
  - "packages/*"
EOF
```

### 26.2 Create web app

```bash
pnpm create next-app apps/web \
  --ts \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*"

cd apps/web
pnpm add lucide-react clsx tailwind-merge zod react-hook-form
cd ../..
```

Add shadcn/ui later if desired:

```bash
cd apps/web
pnpm dlx shadcn@latest init
pnpm dlx shadcn@latest add button card badge tabs dialog dropdown-menu input textarea form separator scroll-area
cd ../..
```

### 26.3 Create API app

Use `uv` if available:

```bash
mkdir -p apps/api/app
cd apps/api
uv init
uv add fastapi uvicorn pydantic pydantic-settings sqlalchemy alembic psycopg[binary] python-dotenv httpx pytest pytest-asyncio
cd ../..
```

Fallback pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pydantic pydantic-settings sqlalchemy alembic "psycopg[binary]" python-dotenv httpx pytest pytest-asyncio
```

### 26.4 Run locally

```bash
docker compose up -d
cd apps/api && uvicorn app.main:app --reload --port 8000
cd apps/web && pnpm dev
```

---

## 27. Claude / Opus build instruction block

Copy this into Claude Code / Opus as the implementation instruction:

```text
You are building the initial open-source skeleton for Mission Control OS from the build plan in this file.

Priorities:
1. Create a working vertical slice, not a perfect system.
2. Mock model responses by default. Do not require OpenAI or Anthropic keys for the demo.
3. Use Next.js + TypeScript for the frontend and FastAPI + SQLAlchemy + Postgres for the backend.
4. Implement the Ideas Forge → Council Room → Best Parts → Blueprint → Mission flow first.
5. Use clean provider interfaces so real OpenAI/Anthropic adapters can be added later.
6. Do not implement dangerous external tool execution.
7. All write/external/deploy/send/delete tools must be disabled or approval-gated by default.
8. Commit useful, readable code with clear README setup instructions.
9. Keep the UI polished enough to understand the product vision.
10. Add TODO comments where P1/P2 features should be connected.

Definition of done:
- `docker compose up -d` starts Postgres/Redis.
- FastAPI runs on localhost:8000.
- Next.js runs on localhost:3000.
- User can create an idea.
- User can run the three-seat council in mock mode.
- User can extract best parts.
- User can generate a blueprint.
- User can promote the blueprint to a mission.
- User can view mission timeline.
- README explains setup and mock mode.
```

---

## 28. API response examples

### Create idea response

```json
{
  "id": "uuid",
  "title": "Mission Control OS",
  "seed_prompt": "Build an agentic mission-control platform...",
  "status": "raw",
  "tags": ["agentic", "open-source", "mission-control"],
  "idea_score": null,
  "risk_score": null,
  "readiness_score": null,
  "created_at": "2026-07-08T00:00:00Z"
}
```

### Council run response

```json
{
  "id": "uuid",
  "idea_id": "uuid",
  "status": "completed",
  "mode": "triad",
  "contributions": [
    {
      "agent_key": "george",
      "agent_name": "George Prime",
      "title": "Control Plane Strategy",
      "summary": "Build the platform around Forge, Council, Blueprint, Mission, Approvals, and Governance.",
      "confidence": 0.89
    },
    {
      "agent_key": "cipher_fable",
      "agent_name": "Cipher Fable",
      "title": "Risk and Governance Challenge",
      "summary": "Default to read-only, approval gates, BBOM, audit logs, and tool blast-radius controls.",
      "confidence": 0.86
    },
    {
      "agent_key": "arty_codex",
      "agent_name": "Arty Codex",
      "title": "Command Center Prototype",
      "summary": "Use agent seat cards, best-parts panels, mission timelines, and a Create from Best Parts button.",
      "confidence": 0.88
    }
  ]
}
```

---

## 29. Testing plan

### Backend tests

```text
test_health.py
  - GET /health returns ok

test_idea_flow.py
  - create idea
  - run council
  - extract best parts
  - generate blueprint
  - promote to mission

test_scoring.py
  - weighted scores are deterministic
  - high risk lowers score
  - high user value increases score

test_council_mock.py
  - mock provider returns all three agent contributions
  - malformed provider output is handled
```

### Frontend tests P1

```text
- Ideas page renders
- New idea form submits
- Idea detail actions work
- Council cards display
- Blueprint panel displays
```

### E2E test P1

Use Playwright:

```text
create idea → run council → extract best parts → generate blueprint → promote to mission
```

---

## 30. Failure handling

Every agent/provider call should handle:

```text
- timeout
- invalid JSON
- provider error
- empty output
- schema validation failure
- rate limit
- missing API key
```

On failure:

```text
- mark step failed
- save error_message
- show error in UI
- allow rerun agent
- do not lose previous successful contributions
```

---

## 31. Future features after skeleton

### Near-term

```text
- Real provider adapters
- Streaming council outputs
- SSE live run timeline
- Langfuse tracing
- Human approval gates connected to tool gateway
- Memory sources
- Export blueprint to Markdown
- Export mission to GitHub issue
```

### Medium-term

```text
- MCP server integration
- Local file workspace for Arty
- PR generation
- GitHub integration
- Slack/Discord bot interface
- Scheduled missions
- Team comments
- Versioned prompts
- Evals and regression tests
```

### Long-term

```text
- Plugin marketplace
- Multi-org SaaS mode
- Self-hosted enterprise mode
- Agent templates
- Tool sandboxing
- Durable workflows with Temporal
- Fine-grained audit/compliance exports
- Mission analytics
- Autonomous low-risk background workers
```

---

## 32. Most important UX copy

Primary product sentence:

```text
Turn rough ideas into agent-reviewed blueprints, then run them as governed missions.
```

Primary button:

```text
Create from Best Parts
```

Secondary buttons:

```text
Run Council
Extract Best Parts
Generate Blueprint
Promote to Mission
Request Cipher Review
Ask Arty to Prototype
```

Status language:

```text
Raw Idea
Council Running
Council Complete
Best Parts Extracted
Blueprint Ready
Mission Draft
Mission Running
Waiting Approval
Completed
```

---

## 33. Non-negotiables

```text
- Mock mode must work without paid API calls.
- Real API keys must never be required for first run.
- External side effects must be disabled by default.
- Tool permissions must be explicit.
- Human approval must exist before real tool execution.
- Every council output must have lineage.
- Every mission run must have a timeline.
- Agent roles must be clear and separable.
- The project should be open-source friendly from day one.
```

---

## 34. Recommended first commit sequence

```text
commit 1: repo scaffold, docker compose, README, license
commit 2: FastAPI app, health route, config
commit 3: DB models, migrations, seed script
commit 4: Next.js app shell, sidebar, dashboard
commit 5: ideas API + ideas UI
commit 6: mock provider + council service
commit 7: council room UI
commit 8: best-parts + blueprint APIs
commit 9: blueprint UI + promote to mission
commit 10: mission detail + timeline
commit 11: approvals/tools/governance placeholder pages
commit 12: tests + README polish
```

---

## 35. Final skeleton acceptance checklist

```text
[ ] Repo has frontend and backend apps
[ ] Docker Compose runs Postgres and Redis
[ ] API health works
[ ] DB migrations work
[ ] Seed script creates George, Fable/Cipher, Arty
[ ] Web dashboard loads
[ ] Ideas list loads
[ ] New idea can be created
[ ] Idea detail loads
[ ] Run Council works in mock mode
[ ] Agent proposals appear
[ ] Best parts can be extracted
[ ] Blueprint can be generated
[ ] Blueprint can be promoted to mission
[ ] Mission detail page shows timeline
[ ] Tools page shows mock tool registry
[ ] Agents page shows BBOM cards
[ ] Approvals page shows placeholder approvals
[ ] README explains setup
[ ] No secrets committed
[ ] License and security notes exist
```

---

## 36. Reference concepts used

This plan draws on these current agentic-system concepts:

```text
- Agentic loop: perception, reasoning, memory, action, feedback
- Multi-agent council patterns
- Human-in-the-loop approvals
- Tool allowlists and tool blast radius
- Behavioral Bill of Materials
- MCP-ready tool gateway
- Trace-first observability
- Open-source safe defaults
```

Useful reference URLs:

```text
Tech Jacks Agentic AI Hub:
https://techjacksolutions.com/ai/agentic-ai/

OpenAI Agents SDK:
https://openai.github.io/openai-agents-python/

OpenAI Agents guide:
https://developers.openai.com/api/docs/guides/agents

Claude Agent SDK docs:
https://code.claude.com/docs/en/agent-sdk/overview

Model Context Protocol tools:
https://modelcontextprotocol.io/specification/2025-06-18/server/tools

Langfuse observability docs:
https://langfuse.com/docs/observability/overview
```

---

# End of build plan

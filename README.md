# Mission Control OS

> Turn rough ideas into agent-reviewed blueprints, then run them as governed missions.

> [!WARNING]
> **Mock mode by default.** Real model providers and real tool execution are
> disabled unless explicitly configured. Do not connect write-capable tools
> (email, deploy, file/DB writes, shell, secrets) without first reviewing the
> approval, audit, and permission controls. See [SECURITY.md](SECURITY.md).

Mission Control OS (MCOS) is an open-source **agentic mission-control platform**.
Ideas become blueprints, blueprints become missions, and a three-seat agent
council collaborates under human oversight.

It is **not** just a chatbot — it is a creation and governance control plane.

## The council

| Seat | Persona | Role |
|---|---|---|
| **George** | Mission Commander | Strategy, architecture, synthesis, final blueprint |
| **Fable / Cipher** | Sentinel | Risk, security, assumptions, failure modes, approval gates |
| **Arty** | Maker | UI/UX, prototype, build scaffold, product feel |

> Seats are **logical roles**, not hardcoded models. Model routing is configured
> via environment variables and provider adapters.

## The vertical slice

```
Create Idea → Run Council (George + Fable/Cipher + Arty) → Extract Best Parts
  → Generate Blueprint → Promote to Mission → View Mission Run Timeline
```

Everything runs in **mock mode by default** — no OpenAI/Anthropic keys required.

## Quickstart

Requirements: **Python 3.12+**, **Node 20+**. No Docker needed for the default
SQLite dev database.

```bash
# 1. Environment
cp env.example .env

# 2. Backend (FastAPI)
cd apps/api
uv venv
uv pip install -e ".[dev]"
python -m app.seed          # seed org, users, agents, tools, sample idea
uvicorn app.main:app --reload --port 8000
# → http://localhost:8000/health  and  http://localhost:8000/docs

# 3. Frontend (Next.js) — in a second terminal
cd apps/web
pnpm install
pnpm dev
# → http://localhost:3000
```

## Mock mode vs real providers

- **Mock mode (default):** `ENABLE_REAL_MODELS=false`, `DEFAULT_MODEL_PROVIDER=mock`.
  Deterministic council outputs so the whole flow works offline and for free.
- **Real providers (later):** set `ENABLE_REAL_MODELS=true`, add
  `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`, and pick models per seat.

## Database

- **Default:** SQLite (`sqlite:///./mcos.db`) — zero install.
- **Postgres (optional):** `docker compose up -d`, then set
  `DATABASE_URL=postgresql+psycopg://mcos:mcos@localhost:5432/mcos`.

## Architecture

```
Next.js Web App → FastAPI Control Plane → Postgres/SQLite
                        │
                        ├─ Agent Orchestrator → Mock / OpenAI / Anthropic adapters
                        ├─ Tool Gateway (mock, MCP-ready)
                        └─ Trace / Audit (internal; Langfuse later)
```

The frontend never calls model providers directly — all model calls go through
the backend.

## Security

MCOS ships with **mock / read-only defaults**. Write, deploy, shell, external
communication, and customer-data tools are disabled or approval-gated by default.
See [SECURITY.md](SECURITY.md).

## Status

Early-stage skeleton. The P0 target is a working mock vertical slice. See the
detailed build plan in [`mission-control-os-build-plan.md`](mission-control-os-build-plan.md).

## Author

Created and maintained by [@jlloyd7](https://github.com/jlloyd7).

## License

[Apache-2.0](LICENSE) © 2026 jlloyd7 and contributors.

## License

[Apache-2.0](LICENSE).

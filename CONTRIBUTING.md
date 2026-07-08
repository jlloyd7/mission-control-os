# Contributing to Mission Control OS

Thanks for your interest! This project is an open-source agentic mission-control
platform. It is early — expect rough edges.

## Ground rules

- **Safe defaults stay safe.** Do not change mock/read-only defaults to
  "real" or "enabled" in committed code. External side effects must remain
  disabled or approval-gated by default.
- **No secrets in the repo.** Use `env.example` as the template. `.env` is
  gitignored.
- **Keep the vertical slice working.** Idea → Council → Best Parts → Blueprint
  → Mission must run in mock mode with no API keys.

## Dev setup

See the [README](README.md) quickstart. In short:

```bash
# Backend (Python 3.12+)
cd apps/api
uv venv && uv pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000

# Frontend (Node 20+)
cd apps/web
pnpm install
pnpm dev
```

## Pull requests

- Keep changes focused and readable.
- Add or update tests for backend behavior changes (`apps/api/tests`).
- Describe user-facing changes clearly.

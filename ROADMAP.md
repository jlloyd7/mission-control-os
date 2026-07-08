# Mission Control OS — Roadmap

Status-first, safety-first. Mock mode always keeps working with no API keys.

## ✅ P0 — Mock vertical slice (done)
Idea → Council → Best Parts → Blueprint → Mission → Timeline → Approvals → Audit,
on SQLite, in mock mode. FastAPI + Next.js, seed data, Alembic, tests.

## 🚧 P1 — Real-model-ready, safe, versioned, publishable (in progress)
- [x] Provider adapters (OpenAI, Anthropic) behind `ENABLE_REAL_MODELS`, per-seat routing
- [x] Agent registry: George, Fable/Cipher, Arty, Opus 4.8, Sonnet 5
- [x] Locked v0 version stamps (council schema / prompt pack / scoring weights)
- [x] CI (backend tests + alembic, frontend typecheck + build, secret scan)
- [ ] Job-style council runs (`queued/running/succeeded/failed/needs_review`), no Redis required
- [ ] Structured-output validation + one repair pass; store raw output; never corrupt canonical tables
- [ ] Version fields persisted on council runs / blueprints / missions
- [ ] Idempotency: no silent duplicate missions; explicit re-run versions
- [ ] Approval Center v1 data model (action type, payload hash, expiry)
- [ ] Screenshots / demo GIF

## 🔜 P2 — George's personal / production profile
- Docker Compose (api + web + Postgres), then Redis, then a background worker
- Real provider keys, staged (George live first, then Fable/Cipher, then Arty)
- Observability (Langfuse / OpenTelemetry), token/cost logging
- Read-only tools, then approval-gated write tools

## 🔒 Not yet (by design)
Real write/deploy/send/delete tools, agent-controlled permissions, mandatory
Postgres/Docker, complex auth. Real tool execution stays disabled until the
Approval Center and audit model are stronger.

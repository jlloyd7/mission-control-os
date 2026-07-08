# Mission Control OS — Build Status (Handoff to George)

**Date:** 2026-07-08 · **Build:** P0 mock vertical slice · **Commit:** `4e1c49f` (local `main`)
**Mode:** mock / SQLite — runs with **no API keys and no Docker**.

This maps the current build against the plan in
[`mission-control-os-build-plan.md`](../mission-control-os-build-plan.md).

---

## TL;DR

The full vertical slice is **built and verified end-to-end**:

```
Create Idea → Run Council (George + Fable/Cipher + Arty) → Extract Best Parts
  → Generate Blueprint → Promote to Mission → View Run Timeline → Approvals → Audit
```

Verified three ways: an HTTP smoke test, an 11-test `pytest` suite, and the
high-res Next.js UI driving the whole flow live in the browser. A production
`next build` and `alembic upgrade head` both pass.

---

## Acceptance checklist (plan §35)

| ✓ | Item |
|---|---|
| ✅ | Repo has frontend and backend apps |
| ➖ | Docker Compose runs Postgres/Redis — *compose file present; **not required** (SQLite dev). Docker now installed if wanted.* |
| ✅ | API health works |
| ✅ | DB migrations work — *Alembic wired + verified; dev uses `create_all`* |
| ✅ | Seed creates George, Fable/Cipher, Arty |
| ✅ | Web dashboard loads |
| ✅ | Ideas list loads |
| ✅ | New idea can be created |
| ✅ | Idea detail loads |
| ✅ | Run Council works in mock mode |
| ✅ | Agent proposals appear |
| ✅ | Best parts can be extracted |
| ✅ | Blueprint can be generated |
| ✅ | Blueprint can be promoted to mission |
| ✅ | Mission detail shows timeline |
| ✅ | Tools page shows mock tool registry |
| ✅ | Agents page shows BBOM cards |
| ✅ | Approvals page shows placeholder approvals |
| ✅ | README explains setup |
| ✅ | No secrets committed |
| ✅ | License + security notes exist |

**20/21 done; the 1 "➖" is intentionally optional** (SQLite replaces the Docker
requirement for first run).

## Build phases (plan §25)

| Phase | Status |
|---|---|
| 0 — Repo bootstrap | ✅ done |
| 1 — Database + seed | ✅ done (16 tables, idempotent seed) |
| 2 — Ideas Forge | ✅ done |
| 3 — Council Room (mock) | ✅ done |
| 4 — Best Parts + Blueprint | ✅ done |
| 5 — Promote to Mission | ✅ done |
| 6 — Approval Center skeleton | ✅ done |
| 7 — Provider adapters (OpenAI/Anthropic) | ○ stubbed behind `ENABLE_REAL_MODELS` (P7) |
| 8 — Observability | ◑ internal traces (run_steps + audit_logs) done; Langfuse deferred |
| 9 — Tool gateway | ◑ registry + approvals present; execution gateway stubbed |
| 10 — OSS polish | ◑ README/LICENSE/SECURITY/CONTRIBUTING done; screenshots/issue templates pending |

---

## Key decisions & deviations from the plan (for review)

These are the places the build **intentionally deviates** from the raw plan —
all reversible, all to keep first-run friction at zero:

1. **Dev DB = SQLite**, not Postgres. Same SQLAlchemy models target both via
   **portable types** (String(36) UUIDs, `JSON` not `JSONB`, no `text[]` — tags
   are JSON, `metadata` mapped to attr `metadata_`). Postgres path is documented
   and one `DATABASE_URL` change away.
2. **Schema created via `create_all` in dev**; **Alembic** wired for prod
   (`apps/api/migrations`, initial migration verified on a fresh DB).
3. **Council runs synchronously** inside the request (async endpoint). Redis/queue
   deferred to P1 — not needed for the mock slice.
4. **Providers: mock only is active.** OpenAI/Anthropic adapters are real classes
   but raise `NotImplementedError` until `ENABLE_REAL_MODELS=true` (P7).
5. **Auth is a dev stub** — a single seeded org/user. RBAC roles deferred to P1.
6. **Stack specifics:** Next.js 16 + React 19 + Tailwind v4 (CSS-first `@theme`),
   FastAPI + SQLAlchemy 2, Python 3.14. Model-id placeholders (`gpt-5.6-sol`,
   `claude-fable-5`) live in `env.example`, unused until P7.

## Verification evidence

- `pytest` → **11 passed** (`apps/api/tests`: health, full idea→mission flow, scoring, mock council)
- HTTP smoke test drives the entire slice through the real API
- `next build` → all 12 routes compile; `tsc --noEmit` clean
- `alembic upgrade head` rebuilds the full 16-table schema on a fresh DB
- Browser: dashboard, forge, idea detail (council/best-parts/blueprint), no console errors

---

## Open questions for George

1. **Postgres now, or keep SQLite as the OSS default?** (Docker is installed; the switch is trivial.)
2. **Real providers next?** Which model goes in which seat, and priority vs. other work?
3. **Publish to GitHub now?** License is set to **Apache-2.0** per your recommendation — confirm.
4. **Council schema / scoring weights** (plan §8, §13) — lock as-is before wiring real models, or revise?

## How to run

```bash
# Backend (SQLite, mock mode)
cd apps/api
uv venv && uv pip install -e ".[dev]"
python -m app.seed
uvicorn app.main:app --reload --port 8000     # :8000/docs

# Frontend (separate terminal)
pnpm --filter web dev                          # :3000
```

Or use the one-command launcher at the repo root: **`./dev.ps1`** (or double-click `dev.cmd`).

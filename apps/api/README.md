# Mission Control OS — API

FastAPI control plane for Mission Control OS.

## Run

```bash
uv venv
uv pip install -e ".[dev]"
python -m app.seed                 # seed org, users, agents, tools, sample idea
uvicorn app.main:app --reload --port 8000
```

- Health: http://localhost:8000/health
- OpenAPI docs: http://localhost:8000/docs

## Layout

```
app/
  main.py         FastAPI entrypoint
  config.py       env-driven settings (mock mode by default)
  db.py           engine / session / Base
  models/         SQLAlchemy models
  schemas/        Pydantic request/response schemas
  routers/        API routes
  services/       orchestration, council, scoring, synthesis, missions
  providers/      mock / OpenAI / Anthropic model adapters
  prompts/        agent prompt pack (markdown)
  seed.py         dev seed data
tests/            pytest suite
```

## Database

SQLite by default (`sqlite:///./mcos.db`). For Postgres, run `docker compose up -d`
at the repo root and set `DATABASE_URL=postgresql+psycopg://mcos:mcos@localhost:5432/mcos`
(install the driver with `uv pip install -e ".[postgres]"`).

## Migrations

Dev uses `create_all` on startup for zero friction. For Postgres/prod, use Alembic
(reads `DATABASE_URL` from settings):

```bash
alembic upgrade head                          # apply migrations
alembic revision --autogenerate -m "message"  # generate a new migration
```

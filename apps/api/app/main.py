"""FastAPI application entrypoint."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .db import init_db
from .routers import (
    agents,
    approvals,
    council,
    governance,
    health,
    ideas,
    missions,
    runs,
    tools,
)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(ideas.router)
app.include_router(council.router)
app.include_router(missions.router)
app.include_router(runs.router)
app.include_router(agents.router)
app.include_router(tools.router)
app.include_router(approvals.router)
app.include_router(governance.router)


@app.get("/", tags=["health"])
def root() -> dict:
    return {
        "service": settings.app_name,
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
    }

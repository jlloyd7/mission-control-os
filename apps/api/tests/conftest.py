"""Pytest fixtures — isolated temp SQLite so tests never touch dev data."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

# Must be set BEFORE any app import (app.db builds its engine at import time).
_TEST_DB = Path(tempfile.gettempdir()) / "mcos_pytest.db"
if _TEST_DB.exists():
    _TEST_DB.unlink()
os.environ["DATABASE_URL"] = f"sqlite:///{_TEST_DB.as_posix()}"
os.environ["ENABLE_REAL_MODELS"] = "false"
os.environ["DEFAULT_MODEL_PROVIDER"] = "mock"

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def client():
    from app.db import init_db
    from app.main import app
    from app.seed import seed

    init_db()
    seed()
    with TestClient(app) as c:
        yield c

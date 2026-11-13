from contextlib import ExitStack

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.engine.backends.registry import get_backend
from app.main import create_app


def _clear_caches() -> None:
    get_settings.cache_clear()
    get_backend.cache_clear()


@pytest.fixture
def make_client(tmp_path, monkeypatch):
    """Build a test client with the fake engine and a temporary data folder."""
    with ExitStack() as stack:

        def _make(base_url: str = "http://127.0.0.1", **env: str) -> TestClient:
            monkeypatch.setenv("BYTEWISE_BACKEND", "fake")
            monkeypatch.setenv("BYTEWISE_DATA_DIR", str(tmp_path))
            for key, value in env.items():
                monkeypatch.setenv(f"BYTEWISE_{key.upper()}", value)
            _clear_caches()
            return stack.enter_context(TestClient(create_app(), base_url=base_url))

        yield _make
    _clear_caches()


@pytest.fixture
def client(make_client) -> TestClient:
    return make_client()

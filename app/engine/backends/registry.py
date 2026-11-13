import logging
import platform
import sys
from functools import lru_cache

from app.config import get_settings
from app.engine.backends.base import Backend
from app.engine.backends.fake_backend import FakeBackend

log = logging.getLogger("bytewise.engine")

BACKEND_NAMES = ("mlx", "torch", "fake")


def detect_backend_name() -> str:
    """Apple Silicon Mac → mlx. Everything else → torch."""
    if sys.platform == "darwin" and platform.machine() == "arm64":
        return "mlx"
    return "torch"


def create_backend(name: str) -> Backend:
    # Real backends are imported only when needed, so missing packages don't crash the app.
    if name == "fake":
        return FakeBackend()
    if name == "mlx":
        from app.engine.backends.mlx_backend import MlxBackend

        return MlxBackend()
    if name == "torch":
        from app.engine.backends.torch_backend import TorchBackend

        return TorchBackend()
    raise ValueError(f"Unknown backend '{name}'. Use one of: {', '.join(BACKEND_NAMES)}")


@lru_cache(maxsize=1)
def get_backend() -> Backend:
    requested = get_settings().backend
    name = requested or detect_backend_name()

    try:
        backend = create_backend(name)
        if backend.is_available():
            return backend
    except ImportError:
        pass  # the backend file or its packages are not installed yet

    if requested:
        raise RuntimeError(
            f"Backend '{name}' is not available on this machine. "
            "Install its packages, or remove BYTEWISE_BACKEND."
        )
    log.warning(
        "Engine '%s' is not installed here, so the FAKE engine is used (test tones, not speech).",
        name,
    )
    return FakeBackend()

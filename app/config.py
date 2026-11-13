from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BYTEWISE_", env_file=".env", extra="ignore")

    # Which engine to use. None = choose automatically for this machine.
    backend: Literal["mlx", "torch", "fake"] | None = None

    # When set, every API request must send it in the X-ByteWise-Token header.
    # The desktop app sets a random one. Empty in local development.
    token: str | None = None

    # Websites allowed to call the API from a browser (the Vite dev server).
    allowed_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # Override where user data is stored (used by tests).
    data_dir: Path | None = None


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

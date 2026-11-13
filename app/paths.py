from pathlib import Path

from platformdirs import user_data_dir

from app.config import get_settings

APP_NAME = "ByteWise"


def data_dir() -> Path:
    """macOS: ~/Library/Application Support/ByteWise · Windows: %LOCALAPPDATA%\\ByteWise"""
    path = get_settings().data_dir or Path(user_data_dir(APP_NAME, appauthor=False))
    path.mkdir(parents=True, exist_ok=True)
    return path


def _subdir(name: str) -> Path:
    path = data_dir() / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def voices_dir() -> Path:
    return _subdir("voices")


def audio_dir() -> Path:
    return _subdir("audio")


def exports_dir() -> Path:
    return _subdir("exports")


def logs_dir() -> Path:
    return _subdir("logs")

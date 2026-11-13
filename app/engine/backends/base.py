from collections.abc import Iterator
from dataclasses import dataclass
from typing import Protocol

import numpy as np
from pydantic import BaseModel, ConfigDict

SAMPLE_RATE = 24_000  # every engine returns float32 mono audio at this rate


class UnknownModelError(ValueError):
    """The requested model does not exist in this backend."""


class ModelInfo(BaseModel):
    model_config = ConfigDict(frozen=True)

    key: str  # "kokoro" | "chatterbox"
    label: str  # shown in the UI
    backend: str  # "mlx" | "torch" | "fake"
    supports_cloning: bool
    installed: bool  # are the model weights on this machine?


class VoiceInfo(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str  # "kokoro:am_puck"
    name: str  # "Puck"
    model: str  # "kokoro"
    language: str = "en-us"
    gender: str | None = None


@dataclass(frozen=True)
class SpeechRequest:
    model: str  # "kokoro" | "chatterbox"
    text: str  # one chunk of text, already cleaned
    voice: str  # preset voice id (e.g. "am_puck") or a path to a reference sample
    speed: float = 1.0
    energy: float = 0.5
    lang: str = "en"


class Backend(Protocol):
    name: str

    def is_available(self) -> bool:
        """Can this backend run on this machine (packages installed, right hardware)?"""
        ...

    def device(self) -> str:
        """Where it runs: "cpu", "cuda", "mlx" …"""
        ...

    def models(self) -> list[ModelInfo]: ...

    def preset_voices(self, model: str) -> list[VoiceInfo]: ...

    def generate(self, req: SpeechRequest) -> Iterator[np.ndarray]:
        """Yield float32 mono audio chunks at SAMPLE_RATE."""
        ...

import time
import zlib
from collections.abc import Iterator

import numpy as np

from app.engine.backends.base import (
    SAMPLE_RATE,
    ModelInfo,
    SpeechRequest,
    UnknownModelError,
    VoiceInfo,
)

_PRESETS = {
    "kokoro": [
        ("am_puck", "Puck", "male"),
        ("af_heart", "Heart", "female"),
        ("bf_emma", "Emma", "female"),
    ],
    "chatterbox": [],  # cloning only, no presets
}


class FakeBackend:
    name = "fake"

    def __init__(self, chunk_delay: float = 0.05) -> None:
        self.chunk_delay = chunk_delay  # pretend each chunk takes time, like a real model

    def is_available(self) -> bool:
        return True

    def device(self) -> str:
        return "cpu"

    def models(self) -> list[ModelInfo]:
        return [
            ModelInfo(
                key="kokoro",
                label="Kokoro (test tones)",
                backend=self.name,
                supports_cloning=False,
                installed=True,
            ),
            ModelInfo(
                key="chatterbox",
                label="Chatterbox (test tones)",
                backend=self.name,
                supports_cloning=True,
                installed=True,
            ),
        ]

    def preset_voices(self, model: str) -> list[VoiceInfo]:
        self._check_model(model)
        return [
            VoiceInfo(id=f"{model}:{voice_id}", name=name, model=model, gender=gender)
            for voice_id, name, gender in _PRESETS[model]
        ]

    def generate(self, req: SpeechRequest) -> Iterator[np.ndarray]:
        self._check_model(req.model)
        if not req.text.strip():
            return

        # Longer text → longer audio, faster speed → shorter audio (like real speech)
        seconds = min(max(len(req.text) * 0.06 / max(req.speed, 0.1), 0.3), 15.0)
        total = int(seconds * SAMPLE_RATE)

        # Each voice gets its own pitch so you can hear voice changes in the UI
        freq = 180 + zlib.crc32(req.voice.encode()) % 120
        t = np.arange(total, dtype=np.float32) / SAMPLE_RATE
        wave = (0.2 * np.sin(2 * np.pi * freq * t)).astype(np.float32)

        # Short fade in/out so it doesn't click
        fade = min(int(0.02 * SAMPLE_RATE), total // 2)
        ramp = np.linspace(0.0, 1.0, fade, dtype=np.float32)
        wave[:fade] *= ramp
        wave[-fade:] *= ramp[::-1]

        step = SAMPLE_RATE // 2  # half-second chunks
        for start in range(0, total, step):
            if self.chunk_delay:
                time.sleep(self.chunk_delay)
            yield wave[start : start + step]

    def _check_model(self, model: str) -> None:
        if model not in _PRESETS:
            raise UnknownModelError(f"Unknown model '{model}'")

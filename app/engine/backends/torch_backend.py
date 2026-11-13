"""Engine for Windows, Linux and Intel Macs, using PyTorch.

Kokoro: fast preset voices. Chatterbox (voice cloning) is used only if installed.
Models load the first time they are used, not at startup.
"""

import importlib.util
import logging
import threading
from collections.abc import Iterator

import numpy as np

from app.engine.backends.base import (
    SAMPLE_RATE,
    ModelInfo,
    SpeechRequest,
    UnknownModelError,
    VoiceInfo,
)

log = logging.getLogger("bytewise.engine.torch")

KOKORO_REPO = "hexgrad/Kokoro-82M"
CHATTERBOX_REPO = "ResembleAI/chatterbox"

# English voices shipped with Kokoro v1.0.
# 1st letter: a = American, b = British. 2nd letter: f = female, m = male.
KOKORO_VOICES = [
    "af_heart", "af_bella", "af_nicole", "af_sarah",
    "am_adam", "am_michael", "am_puck", "am_fenrir",
    "bf_emma", "bf_isabella", "bm_george", "bm_lewis",
]


def _has_package(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def _is_downloaded(repo_id: str) -> bool:
    """True if the model is already in the Hugging Face cache (checks without downloading)."""
    try:
        from huggingface_hub import snapshot_download

        snapshot_download(repo_id, local_files_only=True)
        return True
    except Exception:
        return False


def _to_numpy(audio) -> np.ndarray:
    if hasattr(audio, "detach"):  # torch tensor
        audio = audio.detach().cpu().numpy()
    return np.asarray(audio, dtype=np.float32).reshape(-1)


class TorchBackend:
    name = "torch"

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._kokoro: dict[str, object] = {}  # one pipeline per accent: "a" or "b"
        self._chatterbox = None
        self._device: str | None = None

    # --- Backend interface -------------------------------------------------

    def is_available(self) -> bool:
        return _has_package("torch") and _has_package("kokoro")

    def device(self) -> str:
        if self._device is None:
            import torch

            self._device = "cuda" if torch.cuda.is_available() else "cpu"
        return self._device

    def models(self) -> list[ModelInfo]:
        models = [
            ModelInfo(key="kokoro", label="Kokoro (fast)", backend=self.name,
                      supports_cloning=False, installed=_is_downloaded(KOKORO_REPO)),
        ]
        if _has_package("chatterbox"):
            models.append(
                ModelInfo(key="chatterbox", label="Chatterbox (voice cloning)", backend=self.name,
                          supports_cloning=True, installed=_is_downloaded(CHATTERBOX_REPO))
            )
        return models

    def preset_voices(self, model: str) -> list[VoiceInfo]:
        if model == "kokoro":
            return [
                VoiceInfo(
                    id=f"kokoro:{v}",
                    name=v[3:].capitalize(),
                    model="kokoro",
                    language="en-gb" if v[0] == "b" else "en-us",
                    gender="female" if v[1] == "f" else "male",
                )
                for v in KOKORO_VOICES
            ]
        if model == "chatterbox":
            return []
        raise UnknownModelError(f"Unknown model '{model}'")

    def generate(self, req: SpeechRequest) -> Iterator[np.ndarray]:
        if req.model not in ("kokoro", "chatterbox"):
            raise UnknownModelError(f"Unknown model '{req.model}'")
        if not req.text.strip():
            return
        if req.model == "kokoro":
            yield from self._generate_kokoro(req)
        else:
            yield from self._generate_chatterbox(req)

    # --- Kokoro ------------------------------------------------------------

    def _kokoro_pipeline(self, lang_code: str):
        with self._lock:
            if lang_code not in self._kokoro:
                from kokoro import KPipeline

                log.info("Loading Kokoro (%s) on %s ...", lang_code, self.device())
                self._kokoro[lang_code] = KPipeline(
                    lang_code=lang_code, repo_id=KOKORO_REPO, device=self.device()
                )
            return self._kokoro[lang_code]

    def _generate_kokoro(self, req: SpeechRequest) -> Iterator[np.ndarray]:
        voice = req.voice.removeprefix("kokoro:")
        pipeline = self._kokoro_pipeline("b" if voice.startswith("b") else "a")
        for _graphemes, _phonemes, audio in pipeline(req.text, voice=voice, speed=req.speed):
            if audio is not None:
                yield _to_numpy(audio)

    # --- Chatterbox (voice cloning) -----------------------------------------

    def _chatterbox_model(self):
        with self._lock:
            if self._chatterbox is None:
                from chatterbox.tts import ChatterboxTTS

                log.info("Loading Chatterbox on %s ...", self.device())
                self._chatterbox = ChatterboxTTS.from_pretrained(device=self.device())
            return self._chatterbox

    def _generate_chatterbox(self, req: SpeechRequest) -> Iterator[np.ndarray]:
        model = self._chatterbox_model()
        wav = model.generate(req.text, audio_prompt_path=req.voice, exaggeration=req.energy)
        if model.sr != SAMPLE_RATE:
            raise RuntimeError(f"Chatterbox returned {model.sr} Hz, expected {SAMPLE_RATE} Hz")
        yield _to_numpy(wav)

import numpy as np
import pytest

from app.engine.backends import SpeechRequest, UnknownModelError
from app.engine.backends.fake_backend import FakeBackend


@pytest.fixture
def backend() -> FakeBackend:
    return FakeBackend(chunk_delay=0)


def render(backend: FakeBackend, **kwargs) -> np.ndarray:
    req = SpeechRequest(**{"model": "kokoro", "voice": "am_puck", **kwargs})
    return np.concatenate(list(backend.generate(req)))


def test_audio_format(backend):
    audio = render(backend, text="Hello world.")
    assert audio.dtype == np.float32
    assert audio.ndim == 1
    assert np.abs(audio).max() > 0.01  # not silent


def test_longer_text_gives_longer_audio(backend):
    short = render(backend, text="Hi.")
    long = render(backend, text="This is a much longer sentence for testing.")
    assert len(short) < len(long)


def test_faster_speed_gives_shorter_audio(backend):
    text = "The same sentence at two speeds."
    assert len(render(backend, text=text, speed=1.5)) < len(render(backend, text=text, speed=1.0))


def test_empty_text_gives_no_audio(backend):
    req = SpeechRequest(model="kokoro", text="   ", voice="am_puck")
    assert list(backend.generate(req)) == []


def test_unknown_model(backend):
    req = SpeechRequest(model="nope", text="Hi", voice="x")
    with pytest.raises(UnknownModelError):
        list(backend.generate(req))

"""ByteWise Voice backend."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("bytewise-voice")
except PackageNotFoundError:  # running without `pip install -e .`
    __version__ = "0.0.0"

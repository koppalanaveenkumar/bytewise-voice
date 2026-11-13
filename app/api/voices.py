from fastapi import APIRouter

from app.api.deps import BackendDep
from app.engine.backends import VoiceInfo

router = APIRouter(tags=["voices"])


@router.get("/voices")
def list_voices(backend: BackendDep) -> list[VoiceInfo]:
    return [voice for m in backend.models() for voice in backend.preset_voices(m.key)]

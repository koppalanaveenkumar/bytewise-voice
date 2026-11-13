from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from app import __version__
from app.api.deps import BackendDep
from app.engine.backends import ModelInfo

router = APIRouter(tags=["system"])


class HealthOut(BaseModel):
    status: Literal["ok"] = "ok"
    version: str
    backend: str
    device: str
    models: list[ModelInfo]


@router.get("/health")
def health(backend: BackendDep) -> HealthOut:
    return HealthOut(
        version=__version__,
        backend=backend.name,
        device=backend.device(),
        models=backend.models(),
    )


@router.get("/models")
def list_models(backend: BackendDep) -> list[ModelInfo]:
    return backend.models()

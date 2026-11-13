import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app import __version__
from app.api import health, voices
from app.config import get_settings
from app.engine.backends import get_backend
from app.paths import data_dir
from app.security import ALLOWED_HOSTS, require_token

logging.basicConfig(level=logging.INFO, format="%(levelname)-9s %(name)s - %(message)s")
log = logging.getLogger("bytewise")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    backend = get_backend()
    log.info(
        "ByteWise Voice %s | engine: %s on %s | data: %s",
        __version__,
        backend.name,
        backend.device(),
        data_dir(),
    )
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="ByteWise Voice", version=__version__, lifespan=lifespan)

    # Security (plan 3.8): only localhost, only our own frontend
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api = APIRouter(prefix="/api", dependencies=[Depends(require_token)])
    api.include_router(health.router)
    api.include_router(voices.router)
    app.include_router(api)
    return app


app = create_app()

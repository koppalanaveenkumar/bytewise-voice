from typing import Annotated

from fastapi import Depends

from app.engine.backends import Backend, get_backend

BackendDep = Annotated[Backend, Depends(get_backend)]

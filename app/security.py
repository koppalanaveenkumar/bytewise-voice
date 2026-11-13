import secrets
from typing import Annotated

from fastapi import Header, HTTPException, status

from app.config import get_settings

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


def require_token(x_bytewise_token: Annotated[str | None, Header()] = None) -> None:
    """Reject requests without the right token, when a token is configured."""
    expected = get_settings().token
    if expected is None:
        return
    if x_bytewise_token is None or not secrets.compare_digest(x_bytewise_token, expected):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing or invalid token")

import secrets
from fastapi import Header, HTTPException
from config import settings

def require_api_key(x_api_key: str | None = Header(None)):
    if settings.api_key is None:
        return

    if x_api_key is None or not secrets.compare_digest(x_api_key, settings.api_key):
        raise HTTPException(401, "Invalid or missing API key")

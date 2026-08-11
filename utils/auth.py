import secrets

from fastapi import Header, HTTPException, status

from config import ADMIN_API_KEY


def require_admin_key(x_admin_key: str = Header(...)) -> None:
    if not ADMIN_API_KEY or not secrets.compare_digest(x_admin_key, ADMIN_API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing admin key",
        )

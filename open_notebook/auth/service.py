"""Authentication service: password hashing + JWT issuance/verification."""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import JWTError, jwt
from loguru import logger

try:
    import bcrypt
except ImportError as e:  # pragma: no cover
    raise ImportError("bcrypt is required: uv add bcrypt") from e

# --- Configuration (read once) -------------------------------------------

# openssl rand -hex 32
def _get_jwt_secret() -> str:
    secret = os.environ.get("JWT_SECRET_KEY")
    if not secret:
        # In AUTH_MODE=none/password this module is never called, so a missing
        # secret is only fatal in jwt mode — checked in main.py.
        logger.warning("JWT_SECRET_KEY not set; JWT auth will not work.")
        return "INSECURE-DEV-ONLY-DO-NOT-USE-IN-PRODUCTION"
    return secret


JWT_ALGORITHM = "HS256"
# Access tokens last 7 days; refresh tokens / expiry hardening is Phase 3.
ACCESS_TOKEN_EXPIRE_DAYS = 7


# --- Password hashing (bcrypt directly; passlib has compat issues with
# bcrypt 5.x) -------------------------------------------------------------

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


# --- JWT -----------------------------------------------------------------

def create_access_token(user_id: str, email: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
    }
    return jwt.encode(payload, _get_jwt_secret(), algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Return the JWT payload, or None if invalid/expired."""
    try:
        return jwt.decode(token, _get_jwt_secret(), algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        logger.debug(f"JWT decode failed: {e}")
        return None

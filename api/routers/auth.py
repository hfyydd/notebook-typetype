"""
Authentication router for Open Notebook API.

Provides:
- GET  /auth/status   — legacy: is a deployment password required?
- POST /auth/register — JWT mode: create a new user
- POST /auth/login    — JWT mode: exchange email/password for a JWT
- GET  /auth/me       — JWT mode: current user profile
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, Field
from loguru import logger

from open_notebook.auth.service import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from open_notebook.database.repository import repo_query
from open_notebook.domain.user import User
from open_notebook.utils.encryption import get_secret_from_env

router = APIRouter(prefix="/auth", tags=["auth"])


# --- Legacy status endpoint (kept for backward compat / frontend gating) --

@router.get("/status")
async def get_auth_status():
    """
    Report auth configuration so the frontend knows which login flow to show.
    `auth_mode` reflects AUTH_MODE env var: 'jwt' | 'password' | 'none'.
    """
    import os

    auth_mode = os.environ.get("AUTH_MODE", "none").lower()
    if auth_mode == "jwt":
        return {"auth_enabled": True, "auth_mode": "jwt",
                "message": "User login required (email + password)."}
    if auth_mode == "password":
        pw_set = bool(get_secret_from_env("OPEN_NOTEBOOK_PASSWORD"))
        return {"auth_enabled": pw_set, "auth_mode": "password",
                "message": "Deployment password required."}
    return {"auth_enabled": False, "auth_mode": "none",
            "message": "Authentication is disabled."}


# --- JWT auth schemas ----------------------------------------------------

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    name: str | None = Field(default=None, max_length=80)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
    token_type: str = "bearer"
    user: dict


class MeResponse(BaseModel):
    id: str
    email: EmailStr
    name: str | None = None
    tier: str | None = None


# --- Routes --------------------------------------------------------------

def _ensure_jwt_mode() -> None:
    import os

    if os.environ.get("AUTH_MODE", "none").lower() != "jwt":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User accounts are disabled. Set AUTH_MODE=jwt to enable.",
        )


def _get_default_tier() -> Optional[str]:
    """Return the yaml default_tier for new users (None if managed mode off)."""
    try:
        from open_notebook.ai.model_config import ModelConfigProvider

        provider = ModelConfigProvider.get_instance()
        return provider.get_default_tier() if provider.is_available() else None
    except Exception:
        return None


@router.post("/register", response_model=AuthResponse)
async def register(req: RegisterRequest):
    """Create a new user account and return a JWT."""
    _ensure_jwt_mode()

    existing = await User.get_by_email(req.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email is already registered.",
        )

    # New users start on the yaml default_tier (typically "free"). If managed
    # mode is off, tier stays None.
    default_tier = _get_default_tier()

    user = User(
        email=req.email,
        password_hash=hash_password(req.password),
        name=req.name,
        tier=default_tier,
    )
    await user.save()

    token = create_access_token(user.id, user.email, tier=user.tier)
    logger.info(
        f"New user registered: {user.email} ({user.id}) tier={user.tier}"
    )
    return AuthResponse(token=token, user=user.public())


@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest):
    """Exchange email + password for a JWT."""
    _ensure_jwt_mode()

    user = await User.get_by_email(req.email)
    if not user or not user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )
    if not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    token = create_access_token(user.id, user.email, tier=user.tier)
    logger.info(f"User logged in: {user.email}")
    return AuthResponse(token=token, user=user.public())


async def _default_user_from_token(
    request: "Request",
) -> dict:
    """Extract the JWT payload from the Authorization header (used by /me)."""
    import os

    if os.environ.get("AUTH_MODE", "none").lower() != "jwt":
        raise HTTPException(status_code=400, detail="JWT mode required.")
    # The JWT middleware already validated the token and attached user info to
    # request.state; reuse it instead of re-parsing.
    user_id = getattr(request.state, "user_id", None)
    if user_id:
        return {
            "sub": user_id,
            "email": getattr(request.state, "user_email", None),
        }
    auth = request.headers.get("Authorization", "")
    if not auth.lower().startswith("bearer "):
        raise HTTPException(
            status_code=401, detail="Missing or invalid Authorization header."
        )
    payload = decode_access_token(auth.split(" ", 1)[1].strip())
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return payload


@router.get("/me", response_model=MeResponse)
async def me(payload: dict = Depends(_default_user_from_token)):
    """Return the current authenticated user's profile."""
    return MeResponse(
        id=payload["sub"],
        email=payload["email"],
        name=payload.get("name"),
        tier=payload.get("tier"),
    )

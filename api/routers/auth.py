"""
Authentication router for Open Notebook API.

Provides:
- GET  /auth/status   — legacy: is a deployment password required?
- POST /auth/register — JWT mode: create a new user
- POST /auth/login    — JWT mode: exchange email/password for a JWT
- GET  /auth/me       — JWT mode: current user profile
"""

import os

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, Field
from loguru import logger
from typing import Optional

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
            "tier": getattr(request.state, "user_tier", None),
            "name": None,
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
    """Return the current authenticated user's profile (reads fresh tier from DB)."""
    # JWT carries a tier snapshot from login time; for /me we read the latest
    # tier from the DB so admin upgrades are reflected without re-login.
    user = await User.get_by_email(payload["email"])
    if user:
        return MeResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            tier=user.tier,
        )
    return MeResponse(
        id=payload["sub"],
        email=payload["email"],
        name=payload.get("name"),
        tier=payload.get("tier"),
    )


# --- Tier management (Phase 3 membership) ---------------------------------

class UpdateTierRequest(BaseModel):
    email: EmailStr
    tier: str = Field(min_length=1, max_length=40)


def _require_admin(payload: dict) -> None:
    """Ensure the current JWT user is a platform admin."""
    email = (payload.get("email") or "").lower()
    admin_emails = os.environ.get("ADMIN_EMAILS", "")
    admin_set = {e.strip().lower() for e in admin_emails.split(",") if e.strip()}
    if email not in admin_set:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required.",
        )


@router.put("/tier")
async def update_user_tier(
    req: UpdateTierRequest,
    payload: dict = Depends(_default_user_from_token),
):
    """Admin-only: set a user's model tier."""
    import os

    _ensure_jwt_mode()
    _require_admin(payload)

    # Validate the tier exists in the yaml config (when managed mode is on).
    try:
        from open_notebook.ai.model_config import ModelConfigProvider

        provider = ModelConfigProvider.get_instance()
        if provider.is_available():
            valid_tiers = provider.list_tiers()
            if req.tier not in valid_tiers:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid tier '{req.tier}'. Available: {valid_tiers}",
                )
    except HTTPException:
        raise
    except Exception:
        pass  # managed mode off → any tier string allowed

    user = await User.get_by_email(req.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {req.email} not found.",
        )

    user.tier = req.tier
    await user.save()
    logger.info(
        f"Admin {payload.get('email')} set {user.email} tier → {req.tier}"
    )
    return {"status": "ok", "email": user.email, "tier": user.tier}


@router.get("/tier")
async def my_tier(payload: dict = Depends(_default_user_from_token)):
    """Return the current user's tier + available tiers (reads fresh from DB)."""
    _ensure_jwt_mode()
    user = await User.get_by_email(payload["email"])
    tier = user.tier if user else payload.get("tier")
    available: list[str] = []
    try:
        from open_notebook.ai.model_config import ModelConfigProvider

        provider = ModelConfigProvider.get_instance()
        if provider.is_available():
            available = provider.list_tiers()
    except Exception:
        pass
    return {"tier": tier, "available_tiers": available}

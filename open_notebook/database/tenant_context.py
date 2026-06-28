"""
Per-request tenant context for multi-tenant data isolation.

In JWT (multi-tenant) mode, the auth middleware sets the current user_id on
this contextvar for the duration of the request. ObjectModel.save() reads it
to stamp new records with user_id, and ObjectModel.get_all() reads it to
filter queries by the current tenant.

In other auth modes the contextvar stays unset (None), and the base model
methods behave as before (no tenant filtering) — preserving single-user
deployments.
"""

from __future__ import annotations

from contextvars import ContextVar, Token
from typing import Optional

# Request-scoped current user id. Set by the auth layer / route handlers.
_current_user_id: ContextVar[Optional[str]] = ContextVar(
    "current_user_id", default=None
)

# Request-scoped current user tier (Phase 3 membership). Set alongside
# user_id so provision_langchain_model can pick the right model tier without
# any call-site changes.
_current_tier: ContextVar[Optional[str]] = ContextVar(
    "current_tier", default=None
)


def get_current_user_id() -> Optional[str]:
    """Return the current request's user id, or None if not in a tenant context."""
    return _current_user_id.get()


def set_current_user_id(user_id: Optional[str]) -> None:
    """Set the current request's user id."""
    _current_user_id.set(user_id)


def get_current_tier() -> Optional[str]:
    """Return the current user's model tier, or None if unset."""
    return _current_tier.get()


def set_current_tier(tier: Optional[str]) -> None:
    """Set the current user's model tier."""
    _current_tier.set(tier)


class user_context:
    """Context manager that scopes a block to a given tenant (+ optional tier)."""

    def __init__(self, user_id: Optional[str], tier: Optional[str] = None):
        self.user_id = user_id
        self.tier = tier
        self._user_token: Optional[Token] = None
        self._tier_token: Optional[Token] = None

    def __enter__(self):
        self._user_token = _current_user_id.set(self.user_id)
        self._tier_token = _current_tier.set(self.tier)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._user_token is not None:
            _current_user_id.reset(self._user_token)
        if self._tier_token is not None:
            _current_tier.reset(self._tier_token)
        return False

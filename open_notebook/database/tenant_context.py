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

from contextvars import ContextVar
from typing import Optional

# Request-scoped current user id. Set by the auth layer / route handlers.
_current_user_id: ContextVar[Optional[str]] = ContextVar(
    "current_user_id", default=None
)


def get_current_user_id() -> Optional[str]:
    """Return the current request's user id, or None if not in a tenant context."""
    return _current_user_id.get()


def set_current_user_id(user_id: Optional[str]) -> None:
    """Set the current request's user id."""
    _current_user_id.set(user_id)


class user_context:
    """Context manager / decorator that scopes a block to a given tenant."""

    def __init__(self, user_id: Optional[str]):
        self.user_id = user_id
        self._token = None

    def __enter__(self):
        self._token = _current_user_id.set(self.user_id)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._token is not None:
            _current_user_id.reset(self._token)
        return False

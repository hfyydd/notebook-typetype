"""User domain model for the multi-tenant cloud-service mode."""

from datetime import datetime
from typing import ClassVar, Optional

from pydantic import EmailStr, field_validator

from open_notebook.database.repository import repo_query
from open_notebook.domain.base import ObjectModel
from open_notebook.exceptions import InvalidInputError, NotFoundError


class User(ObjectModel):
    """An end user. Only used in JWT (multi-tenant) auth mode.

    Email is the unique login identifier. Password is stored hashed via
    bcrypt in password_hash; the plaintext is never persisted.
    """

    table_name: ClassVar[str] = "user"
    tenant_scoped: ClassVar[bool] = False  # users are not filtered by user_id

    email: EmailStr
    password_hash: str
    name: Optional[str] = None
    # Reserved for Phase 3 (membership). Today every user shares default_tier.
    tier: Optional[str] = None

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v):
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @classmethod
    async def get_by_email(cls, email: str) -> Optional["User"]:
        """Find a user by email. Returns None if not found."""
        normalized = email.strip().lower()
        result = await repo_query(
            "SELECT * FROM user WHERE email = $email LIMIT 1",
            {"email": normalized},
        )
        if result:
            return cls(**result[0])
        return None

    @classmethod
    async def get(cls, id: str) -> "User":  # type: ignore[override]
        """Fetch a user by record id."""
        result = await repo_query(
            "SELECT * FROM $id", {"id": __import__("open_notebook.database.repository", fromlist=["ensure_record_id"]).ensure_record_id(id)}
        )
        if not result:
            raise NotFoundError(f"user with id {id} not found")
        return cls(**result[0])

    def public(self) -> dict:
        """Return a dict with no sensitive fields, for API responses."""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "tier": self.tier,
            "created": self.created.isoformat() if self.created else None,
        }

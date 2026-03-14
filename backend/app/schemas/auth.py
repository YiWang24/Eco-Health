"""Authentication schema types."""

from pydantic import BaseModel


class AuthContext(BaseModel):
    user_id: str
    email: str | None = None

"""User context utilities for authenticated requests."""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.schemas.auth import AuthContext


def ensure_user(db: Session, auth: AuthContext) -> User:
    """Ensure an app user row exists for the authenticated principal."""

    def _sync_email(existing: User) -> User:
        if auth.email and existing.email != auth.email:
            existing.email = auth.email
            db.add(existing)
            db.commit()
            db.refresh(existing)
        return existing

    user = db.get(User, auth.user_id)
    if user:
        return _sync_email(user)

    user = User(id=auth.user_id, email=auth.email)
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        # Concurrent requests may race to create the same user row.
        db.rollback()
        existing = db.get(User, auth.user_id)
        if existing:
            return _sync_email(existing)
        raise

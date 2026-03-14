"""User context utilities for authenticated requests."""

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import AuthContext


def ensure_user(db: Session, auth: AuthContext) -> User:
    """Ensure an app user row exists for the authenticated principal."""

    user = db.get(User, auth.user_id)
    if user:
        if auth.email and user.email != auth.email:
            user.email = auth.email
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    user = User(id=auth.user_id, email=auth.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

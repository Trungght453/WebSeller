from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password, verify_password


def register_user(db: Session, email: str, password: str) -> User:
    # IMPORTANT: password is RAW STRING
    user = User(
        email=email,
        hashed_password=hash_password(password),
        is_admin=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

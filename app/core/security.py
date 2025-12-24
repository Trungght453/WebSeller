from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash RAW password only.
    Accepts simple passwords like '123'.
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string")

    # Reject already-hashed passwords (THIS PREVENTS YOUR BUG)
    if password.startswith("$2a$") or password.startswith("$2b$"):
        raise ValueError("hash_password received a hashed password")

    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

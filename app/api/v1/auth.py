from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import register_user, authenticate_user
from app.core.security import create_access_token
from app.db.session import get_db

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    # 🔥 THIS LINE WAS YOUR ROOT BUG BEFORE
    user = register_user(
        db=db,
        email=payload.email,
        password=payload.password,  # RAW STRING ONLY
    )

    return {"id": user.id, "email": user.email}


@router.post("/login")
def login(
    payload: UserLogin,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db,
        email=payload.email,
        password=payload.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}

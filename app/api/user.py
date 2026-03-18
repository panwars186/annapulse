import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.deps import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = (
            db.query(User)
            .filter(User.phone_number == user.phone_number)
            .first()
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to check for existing user with phone=%s", user.phone_number)
        raise HTTPException(status_code=500, detail="Failed to create user") from exc

    if existing_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    new_user = User(**user.model_dump())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:  # noqa: BLE001
        logger.exception("Failed to create user with phone=%s", user.phone_number)
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create user")

    return new_user


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return current_user

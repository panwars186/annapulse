from fastapi import APIRouter ,Depends,HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.schemas.user import UserCreate,UserResponse
from app.models.user import User
from app.db.deps import get_db

router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/",response_model=UserResponse)
def create_user(user:UserCreate,db:Session=Depends(get_db)):
    existing_user = db.query(User).filter(User.phone_number == user.phone_number).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="phone number already registered")
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/me")
def get_me(current_user = get_current_user):
    return current_user



from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.deps import get_db
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate

router = APIRouter(prefix="/feedback",tags=["Feedback"])

@router.post("/feedback")
def give_feedback(
    feedback:FeedbackCreate,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)):
    new_feedback = Feedback(
        user_id =current_user.id,
        meal_id  = feedback.meal_id,
        rating = feedback.rating,
        comment = feedback.comment
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback


@router.get("/feedback")
def get_feedback(db:Session =Depends(get_db)):
    feedback = db.query(Feedback).all

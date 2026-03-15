from datetime import timedelta, datetime, timezone
from http.client import HTTPException

from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter

from app.db.deps import get_db
from app.models.meal_schedule import MealSchedule
from app.schemas.meal import SkilMealRequest

router =APIRouter(prefix="/meals",tags=["Meals"])

@router.post("/skip")
def skip_meal(
    data: SkilMealRequest,
    db: Session = Depends(get_db)):

    meal = db.query(MealSchedule).filter(MealSchedule.id == data.schedule_id).first()
    if not meal:
        raise HTTPException(status_code = 404,details = "Meal Not found")

    lock_time = meal.delivery_date -timedelta(hours=12)
    if datetime.now(timezone.utc) >lock_time:
        raise HTTPException(status_code=400, details = "Meal Locked , Cannot skip within 12 hours of delivery")
    meal.status = "SKIPPED"
    db.commit()
    return {"message":"Meal skipped successfully"}



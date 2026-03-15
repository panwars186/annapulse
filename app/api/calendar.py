from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.deps import get_db
from app.models.meal_schedule import  MealSchedule
from app.services.meal_lock import is_meal_locked

router = APIRouter(prefix = "/calendar",tags=["Meal Calendar"])

@router.get("/")
def get_calendar(
    db:Session =Depends(get_db),
    current_user = Depends(get_current_user)):
    meals = db.query(MealSchedule).filter(MealSchedule.user_id == current_user.id).all()
    return meals

    # Fetch meals for the current user and return them in a calendar format
@router.post("/skip")
def skip_meal(
    delivery_date:str,
    meal_type:str,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)
    ):
    meal = (db.query(MealSchedule).filter/
            (MealSchedule.id == current_user.id,
             MealSchedule.delivery_date==delivery_date,
             MealSchedule.meal_type == meal_type).first())
    if not meal:
        raise HTTPException(status_code=404,detail="Meal not Found")
    if is_meal_locked(meal.date,meal.meal_type):
        raise HTTPException(status_code=400,detail="Meal Locked, Cannot skip within 12 hours of delivery")
    meal.status = "SKIPPED"
    db.commit()

    return{"message":"Meal skipped successfully"}

@router.post("/skip_day")
def skip_day(
    delivery_date:str,
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)):
    meals = db.query(MealSchedule).filter(
        MealSchedule.user_id == current_user.id,
        MealSchedule.delivery_date == delivery_date
    ).all()
    if not meals:
        raise HTTPException(status_code=404,detail="No meals found for the specified date")

    for meal in meals:
        meal.status= "SKIPPED"
    db.commit()

    return {"message":"All meals for the day skipped successfully"}

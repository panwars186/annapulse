from datetime import date

import dateutil.utils
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.meal_schedule import MealSchedule
from app.models.notification import Notification
from app.models.user import User

router = APIRouter(prefix="/delivery",tags=["Delivery"])

router.get("/today_deliveries")
def today_deliveries(db:Session= Depends(get_db)):
    today = date.today()
    meals = db.query(MealSchedule).filter(
    MealSchedule.delivery_date == today,
    MealSchedule.status == "Scheduled"
    ).all()
    delivery_list = []
    for meal in meals:
        user = db.query(User).filter(User.id == meal.user_id).first()
        delivery_list.append({
        "user_id":user.id,
        "name":user.name,
        "address":user.address,
        "meal_type":meal.meal_type,
        "meal_id":meal.id
        })
        return delivery_list

@router.post("/mark_delivered/{meal_id}")
def mark_delivered(meal_id:int,db:Session =Depends(get_db)):
    meal = db.query(MealSchedule).filter(MealSchedule.id == meal_id).first()
    if not meal:
        return {"message":"Meal not found"}

    meal.status = "delivered"

    notification = Notification(
    user_id = meal.user_id,
    title = "Meal Delivered",
    message = f"Your {meal.meal_type} meal has been delivered today. Enjoy your meal!"
    )
    db.add(notification)
    db.commit()


    return {"message":"Meal delivered successfully"}




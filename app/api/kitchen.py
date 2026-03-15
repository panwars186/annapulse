from collections import defaultdict
from datetime import timedelta, date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.meal_schedule import MealSchedule
from app.models.user import User

router = APIRouter(prefix="/kitchen",tags=["Kitchen"])

@router.get("/tomorrow_meals")
def tomorrow_meals(db:Session = Depends(get_db)):
    tomorrow = date.today()+timedelta(days=1)
    meals = db.query(MealSchedule,User).join(User,MealSchedule.user_id == User.id).filter(MealSchedule.date == tomorrow,MealSchedule.status == "Scheduled").all()
    result = []
    for meal, user in meals:
        result.append({
            "meal_type":meal.meal_type,
            "customer":user.name,
            "phone":user.phone,
            "address":user.address
        })
    return result

@router.get("/delivery-routes")
def delivery_routes(db:Session=Depends(get_db)):
    tomorrow = date.today()+ timedelta(days=1)
    meals = db.query(MealSchedule,User).join(User,MealSchedule.user_id == User.id).filter(
        MealSchedule.date == tomorrow,
        MealSchedule.status == "Scheduled").all()
    routes = defaultdict(list)
    for meal, user in meals:
        routes[user.area].append({
        "customer": user.name,
        "phone": user.phone,
        "address": user.address,
        "meal_type": meal.meal_type
        })
    return routes
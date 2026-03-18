import logging
from collections import defaultdict
from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.meal_schedule import MealSchedule
from app.models.user import User

router = APIRouter(prefix="/kitchen", tags=["Kitchen"])
logger = logging.getLogger(__name__)


@router.get("/tomorrow_meals")
def tomorrow_meals(db: Session = Depends(get_db)):
    tomorrow = date.today() + timedelta(days=1)
    try:
        meals = (
            db.query(MealSchedule, User)
            .join(User, MealSchedule.user_id == User.id)
            .filter(
                MealSchedule.delivery_date == tomorrow,
                MealSchedule.status == "Scheduled",
            )
            .all()
        )
    except Exception:  # noqa: BLE001
        logger.exception("Failed to fetch kitchen meals for %s", tomorrow)
        raise HTTPException(status_code=500, detail="Failed to fetch meals")

    result = []
    for meal, user in meals:
        result.append(
            {
                "meal_type": meal.meal_type,
                "customer": user.name,
                "phone": user.phone,
                "address": user.address,
            }
        )
    return result


@router.get("/delivery-routes")
def delivery_routes(db: Session = Depends(get_db)):
    tomorrow = date.today() + timedelta(days=1)
    try:
        meals = (
            db.query(MealSchedule, User)
            .join(User, MealSchedule.user_id == User.id)
            .filter(
                MealSchedule.delivery_date == tomorrow,
                MealSchedule.status == "Scheduled",
            )
            .all()
        )
    except Exception:  # noqa: BLE001
        logger.exception("Failed to fetch delivery routes for %s", tomorrow)
        raise HTTPException(status_code=500, detail="Failed to fetch delivery routes")

    routes = defaultdict(list)
    for meal, user in meals:
        routes[user.area].append(
            {
                "customer": user.name,
                "phone": user.phone,
                "address": user.address,
                "meal_type": meal.meal_type,
            }
        )
    return routes

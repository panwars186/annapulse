import logging
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.meal_schedule import MealSchedule
from app.models.notification import Notification
from app.models.user import User

router = APIRouter(prefix="/delivery", tags=["Delivery"])
logger = logging.getLogger(__name__)


@router.get("/today_deliveries")
def today_deliveries(db: Session = Depends(get_db)):
    today = date.today()
    try:
        meals = (
            db.query(MealSchedule)
            .filter(
                MealSchedule.delivery_date == today,
                MealSchedule.status == "Scheduled",
            )
            .all()
        )
    except Exception:  # noqa: BLE001
        logger.exception("Failed to fetch today's deliveries for %s", today)
        raise HTTPException(status_code=500, detail="Failed to fetch deliveries")

    delivery_list = []
    for meal in meals:
        user = db.query(User).filter(User.id == meal.user_id).first()
        if not user:
            logger.warning("User not found for meal_id=%s, user_id=%s", meal.id, meal.user_id)
            continue

        delivery_list.append(
            {
                "user_id": user.id,
                "name": user.name,
                "address": user.address,
                "meal_type": meal.meal_type,
                "meal_id": meal.id,
            }
        )

    return delivery_list


@router.post("/mark_delivered/{meal_id}")
def mark_delivered(meal_id: int, db: Session = Depends(get_db)):
    try:
        meal = (
            db.query(MealSchedule)
            .filter(MealSchedule.id == meal_id)
            .first()
        )
    except Exception:  # noqa: BLE001
        logger.exception("Failed to load meal_id=%s for delivery update", meal_id)
        raise HTTPException(status_code=500, detail="Failed to update meal delivery status")

    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    meal.status = "DELIVERED"

    notification = Notification(
        user_id=meal.user_id,
        title="Meal Delivered",
        message=f"Your {meal.meal_type} meal has been delivered today. Enjoy your meal!",
    )
    try:
        db.add(notification)
        db.commit()
    except Exception:  # noqa: BLE001
        logger.exception("Failed to mark meal as delivered for meal_id=%s", meal_id)
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to mark meal as delivered")

    return {"message": "Meal delivered successfully"}

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.deps import get_db
from app.models.meal_schedule import MealSchedule
from app.services.meal_lock import is_meal_locked

router = APIRouter(prefix="/calendar", tags=["Meal Calendar"])
logger = logging.getLogger(__name__)


@router.get("/")
def get_calendar(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        meals = (
            db.query(MealSchedule)
            .filter(MealSchedule.user_id == current_user.id)
            .all()
        )
    except Exception:  # noqa: BLE001
        logger.exception("Failed to fetch calendar for user_id=%s", current_user.id)
        raise HTTPException(status_code=500, detail="Failed to fetch meal calendar")

    return meals


@router.post("/skip")
def skip_meal(
    delivery_date: str,
    meal_type: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        meal = (
            db.query(MealSchedule)
            .filter(
                MealSchedule.user_id == current_user.id,
                MealSchedule.delivery_date == delivery_date,
                MealSchedule.meal_type == meal_type,
            )
            .first()
        )
    except Exception:  # noqa: BLE001
        logger.exception(
            "Failed to load meal for skip: user_id=%s, date=%s, type=%s",
            current_user.id,
            delivery_date,
            meal_type,
        )
        raise HTTPException(status_code=500, detail="Failed to skip meal")

    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    if is_meal_locked(meal.delivery_date, meal.meal_type):
        raise HTTPException(
            status_code=400,
            detail="Meal locked, cannot skip within 12 hours of delivery",
        )

    meal.status = "SKIPPED"
    db.commit()

    return {"message": "Meal skipped successfully"}


@router.post("/skip_day")
def skip_day(
    delivery_date: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        meals = (
            db.query(MealSchedule)
            .filter(
                MealSchedule.user_id == current_user.id,
                MealSchedule.delivery_date == delivery_date,
            )
            .all()
        )
    except Exception:  # noqa: BLE001
        logger.exception(
            "Failed to load meals for skip_day: user_id=%s, date=%s",
            current_user.id,
            delivery_date,
        )
        raise HTTPException(status_code=500, detail="Failed to skip meals for day")

    if not meals:
        raise HTTPException(
            status_code=404,
            detail="No meals found for the specified date",
        )

    for meal in meals:
        meal.status = "SKIPPED"

    db.commit()

    return {"message": "All meals for the day skipped successfully"}


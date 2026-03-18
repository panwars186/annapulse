import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.meal_schedule import MealSchedule
from app.schemas.meal import SkilMealRequest

router = APIRouter(prefix="/meals", tags=["Meals"])
logger = logging.getLogger(__name__)


@router.post("/skip")
def skip_meal(
    data: SkilMealRequest,
    db: Session = Depends(get_db),
):
    try:
        meal = (
            db.query(MealSchedule)
            .filter(MealSchedule.id == data.schedule_id)
            .first()
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to load meal schedule_id=%s", data.schedule_id)
        raise HTTPException(status_code=500, detail="Failed to skip meal") from exc

    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    lock_time = meal.delivery_date - timedelta(hours=12)
    if datetime.now(timezone.utc) > lock_time:
        raise HTTPException(
            status_code=400,
            detail="Meal locked, cannot skip within 12 hours of delivery",
        )

    meal.status = "SKIPPED"
    db.commit()

    return {"message": "Meal skipped successfully"}


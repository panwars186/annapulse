import logging
from datetime import timedelta
from typing import Iterable

from sqlalchemy.orm import Session

from app.models.meal_schedule import MealSchedule
from app.models.subscription import Subscription

logger = logging.getLogger(__name__)


def generate_meals(
    db: Session,
    subscription: Subscription,
    meal_types: str,
    duration: int,
) -> None:
    meal_list: Iterable[str] = [m.strip() for m in meal_types.split(",") if m.strip()]

    try:
        for day in range(duration):
            delivery_date = subscription.start_date + timedelta(days=day)
            for meal_type in meal_list:
                meal = MealSchedule(
                    user_id=subscription.user_id,
                    subscription_id=subscription.id,
                    meal_type=meal_type,
                    delivery_date=delivery_date,
                )

                db.add(meal)

        logger.info(
            "Generated meals for subscription_id=%s, duration=%s, types=%s",
            subscription.id,
            duration,
            list(meal_list),
        )
    except Exception:  # noqa: BLE001
        logger.exception(
            "Failed generating meals for subscription_id=%s",
            subscription.id,
        )
        raise

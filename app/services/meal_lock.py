from datetime import date, datetime, time, timedelta
from typing import Literal

MealType = Literal["Breakfast", "Lunch", "Dinner"]


def is_meal_locked(meal_date: date, meal_type: MealType) -> bool:
    """
    Determine if a meal is locked based on its type and date.

    Business rules:
    - Breakfast: locked from 18:00 the previous day
    - Lunch:     locked from 07:00 on the same day
    - Dinner:    locked from 13:00 on the same day
    """
    now = datetime.now()

    if meal_type == "Breakfast":
        lock_time = datetime.combine(meal_date - timedelta(days=1), time(18, 0))
    elif meal_type == "Lunch":
        lock_time = datetime.combine(meal_date, time(7, 0))
    elif meal_type == "Dinner":
        lock_time = datetime.combine(meal_date, time(13, 0))
    else:
        # Fallback: treat unknown types as unlocked
        return False

    return now > lock_time

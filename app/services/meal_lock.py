from datetime import datetime, timedelta, time


def is_meal_locked(meal_date,meal_type):
    now = datetime.now()
    if meal_type == "breakfast":
        lock_time = datetime.combine(meal_date-timedelta(days=1),time(18,0))

    elif meal_type == "lunch":
        lock_time = datetime.combine(meal_date,time(7,0))

    elif meal_type == "dinner":
        lock_time = datetime.combine(meal_date,time(13,0))

    else:
        return False

    return now>lock_time


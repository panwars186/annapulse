from datetime import timedelta

from app.models.meal_schedule import MealSchedule


def generate_meals(db,subscription,meal_types,duration):
    meal_list = meal_types.split(",")
    for day in range(duration):
        delivery_date = subscription.start_date+timedelta(days=day)
        for meal_type in meal_list:
            meal = MealSchedule(
                user_id=subscription.user_id,
                subscription_id=subscription.id,
                meal_type=meal_type,
                delivery_date=delivery_date
            )

            db.add(meal)
    db.commit()
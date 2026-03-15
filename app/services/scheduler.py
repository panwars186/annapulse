from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.subscription import Subscription
from app.services.billing import deduct_daily_meal_cost
from app.services.meal_processor import process_today_meal


def run_daily_billing():
    db:Session =SessionLocal()
    subscriptions = db.query(Subscription).filter(Subscription.status == "ACTIVE").all()
    for sub in subscriptions:
        deduct_daily_meal_cost(db,sub)

    db.close()

scheduler  = BackgroundScheduler()
scheduler.add_job(
    run_daily_billing,
    "cron",
    hour = 3, minute = 0
)

scheduler.add_job(
    process_today_meal,
    "cron",
    hour = 5,
    minute=0
)
# scheduler.start()
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.subscription import Subscription
from app.services.billing import deduct_daily_meal_cost
from app.services.meal_processor import process_today_meal

logger = logging.getLogger(__name__)


def run_daily_billing() -> None:
    db: Session = SessionLocal()
    try:
        subscriptions = (
            db.query(Subscription)
            .filter(Subscription.status == "ACTIVE")
            .all()
        )
        for sub in subscriptions:
            deduct_daily_meal_cost(db, sub)

        db.commit()
    except Exception:  # noqa: BLE001
        logger.exception("Failed to run daily billing job")
        db.rollback()
        raise
    finally:
        db.close()


scheduler = BackgroundScheduler()
scheduler.add_job(
    run_daily_billing,
    "cron",
    hour=3,
    minute=0,
)

scheduler.add_job(
    process_today_meal,
    "cron",
    hour=5,
    minute=0,
)

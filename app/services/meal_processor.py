import logging
from datetime import date

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.meal_schedule import MealSchedule
from app.models.wallet import Wallet
from app.models.wallet_transaction import WalletTransaction

logger = logging.getLogger(__name__)


def process_today_meal() -> None:
    db: Session = SessionLocal()
    today = date.today()

    try:
        meals = (
            db.query(MealSchedule)
            .filter(
                MealSchedule.delivery_date == today,
                MealSchedule.status == "SCHEDULED",
            )
            .all()
        )

        for meal in meals:
            wallet = db.query(Wallet).filter(Wallet.user_id == meal.user_id).first()
            if wallet is None:
                logger.warning("Wallet not found for user_id=%s", meal.user_id)
                continue

            if wallet.balance < meal.price:
                logger.info(
                    "Insufficient balance for user_id=%s, meal_id=%s",
                    meal.user_id,
                    meal.id,
                )
                continue

            wallet.balance -= meal.price
            transaction = WalletTransaction(
                user_id=meal.user_id,
                amount=meal.price,
                transaction_type="DEBIT",
                description=f"Payment for meal {meal.id} on {meal.delivery_date}",
            )
            db.add(transaction)
            meal.status = "DELIVERED"

        db.commit()
    except Exception:  # noqa: BLE001
        logger.exception("Failed to process today's meals for %s", today)
        db.rollback()
        raise
    finally:
        db.close()

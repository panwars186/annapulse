from datetime import date
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.meal_schedule import MealSchedule
from app.models.subscription import Subscription
from app.models.wallet import Wallet
from app.models.wallet_transaction import WalletTransaction

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])
logger = logging.getLogger(__name__)


def _get_today() -> date:
    """Return today's date. Extracted for easier testing and consistency."""
    return date.today()


def _get_meal_count_by_type(
    db: Session, meal_type: str, delivery_date: date | None = None, status: str = "Scheduled"
) -> int:
    """Return count of meals for a given type, date, and status."""
    delivery_date = delivery_date or _get_today()
    try:
        return (
            db.query(MealSchedule)
            .filter(
                MealSchedule.delivery_date == delivery_date,
                MealSchedule.meal_type == meal_type,
                MealSchedule.status == status,
            )
            .count()
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to fetch %s meal count for %s", meal_type, delivery_date)
        raise HTTPException(status_code=500, detail="Failed to fetch meal count") from exc


@router.get("/today_orders")
def today_orders(db: Session = Depends(get_db)):
    today = _get_today()

    try:
        # Query once for all scheduled meals for today, then aggregate in Python.
        meals = (
            db.query(MealSchedule)
            .filter(
                MealSchedule.delivery_date == today,
                MealSchedule.status == "Scheduled",
            )
            .all()
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to fetch today's meals for %s", today)
        raise HTTPException(status_code=500, detail="Failed to fetch today's orders") from exc

    breakfast = 0
    lunch = 0
    dinner = 0

    for meal in meals:
        if meal.meal_type == "Breakfast":
            breakfast += 1
        elif meal.meal_type == "Lunch":
            lunch += 1
        elif meal.meal_type == "Dinner":
            dinner += 1

    return {
        "date": today,
        "breakfast_orders": breakfast,
        "lunch_orders": lunch,
        "dinner_orders": dinner,
    }


@router.get("/breakfast_orders")
def breakfast_orders(db: Session = Depends(get_db)):
    count = _get_meal_count_by_type(db, meal_type="Breakfast")
    return {"breakfast_orders": count}


@router.get("/lunch_orders")
def lunch_orders(db: Session = Depends(get_db)):
    count = _get_meal_count_by_type(db, meal_type="Lunch")
    return {"lunch_orders": count}


@router.get("/dinner_orders")
def dinner_orders(db: Session = Depends(get_db)):
    count = _get_meal_count_by_type(db, meal_type="Dinner")
    return {"dinner_orders": count}


@router.get("/revenue_today")
def revenue_today(db: Session = Depends(get_db)):
    today = _get_today()
    try:
        transactions = (
            db.query(WalletTransaction)
            .filter(
                WalletTransaction.transaction_type == "DEBIT",
                WalletTransaction.created_at >= today,
            )
            .all()
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to fetch revenue for %s", today)
        raise HTTPException(status_code=500, detail="Failed to fetch today's revenue") from exc

    revenue = sum(t.amount for t in transactions)
    return {"Today's Revenue": revenue}


@router.get("/active_subscribers")
def active_subscribers(db: Session = Depends(get_db)):
    today = _get_today()
    try:
        active = db.query(Subscription).filter(Subscription.status == "ACTIVE").count()
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to fetch active subscribers for %s", today)
        raise HTTPException(status_code=500, detail="Failed to fetch active subscribers") from exc

    return {f"Total Active Subscribers on {today}": active}


@router.get("/meals_delivered")
def meals_delivered(db: Session = Depends(get_db)):
    today = _get_today()
    try:
        meals = (
            db.query(MealSchedule)
            .filter(
                MealSchedule.delivery_date == today,
                MealSchedule.status == "DELIVERED",
            )
            .count()
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to fetch delivered meals for %s", today)
        raise HTTPException(status_code=500, detail="Failed to fetch delivered meals") from exc

    return {"Meals Delivered Today": meals}


@router.get("/wallet_balance")
def wallet_balance(db: Session = Depends(get_db)):
    try:
        wallets = db.query(Wallet).all()
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to fetch wallet balances")
        raise HTTPException(status_code=500, detail="Failed to fetch wallet balances") from exc

    total = sum(wallet.balance for wallet in wallets)
    return {"Total Wallet Balance": total}

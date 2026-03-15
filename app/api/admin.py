from datetime import date

import dateutil.utils
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.meal_schedule import MealSchedule
from app.models.subscription import Subscription
from app.models.wallet import Wallet
from app.models.wallet_transaction import WalletTransaction

router = APIRouter(prefix = "/admin", tags=["Admin Dashboard"])

@router.get("/today_orders")
def today_orders(db:Session = Depends(get_db)):
    today = date.today()

    meals = db.query(MealSchedule).filter(MealSchedule.delivery_date == today,MealSchedule.status=="Scheduled").all()
    breakfast = 0
    lunch = 0
    dinner = 0

    for meal in meals:
        if meal.meal_type == "Breakfast":
            breakfast +=1
        elif meal.meal_type == "Lunch":
            lunch +=1
        elif meal.meal_type == "Dinner":
            dinner +=1

        return {
        "date": today,
        "breakfast_orders": breakfast,
        "lunch_orders": lunch,
        "dinner_orders": dinner
        }

@router.get("/breakfast_orders")
def breakfast_orders(db:Session = Depends(get_db)):
    today = date.today()
    count = db.query(MealSchedule).filter(
    MealSchedule.delivery_date ==today,
    MealSchedule.meal_type == "Breakfast",
    MealSchedule.status == "Scheduled"
    ).count()
    return {"breakfast_orders": count}

@router.get("/lunch_orders")
def lunch_orders(db:Session = Depends(get_db)):
    today = date.today()
    count = db.query(MealSchedule).filter(
    MealSchedule.delivery_date ==today,
    MealSchedule.meal_type == "Lunch",
    MealSchedule.status == "Scheduled"
    ).count()
    return {"lunch_orders": count}

@router.get("/dinner_orders")
def dinner_orders(db:Session = Depends(get_db)):
    today = date.today()
    count = db.query(MealSchedule).filter(
    MealSchedule.delivery_date ==today,
    MealSchedule.meal_type == "Dinner",
    MealSchedule.status == "Scheduled"
    ).count()
    return {"dinner_orders": count}

@router.get("/revenue_today")
def revenue_today(db:Session = Depends(get_db)):
    today = date.today()
    transactions = db.query(WalletTransaction).filter(WalletTransaction.transaction_type == "DEBIT",
        WalletTransaction.created_at >= today ).all()
    revenue = sum(t.amount for t in transactions)
    return {"Today's Revenue": revenue}

@router.get("/active_subscribers")
def active_subscribers(db:Session = Depends(get_db)):
    active = db.query(Subscription).filter(Subscription.status == "ACTIVE").count()
    return {"Total Active Subscribers on {date.today()}": active}

@router.get("/meals_delivered")
def meals_delivered(db:Session=Depends(get_db)):
    today = date.today()

    meals =db.query(MealSchedule).filter(MealSchedule.date == today,
                MealSchedule.status == "DELIVERED").count()
    return {"Meals Delivered Today": meals}


@router.get("/wallet_balance")
def wallet_balance(db:Session = Depends(get_db)):
    wallets = db.query(Wallet).all()
    total = sum(wallet.balance for wallet in wallets)
    return {"Total Wallet Balance": total}











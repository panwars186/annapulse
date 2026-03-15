from datetime import date

from sqlalchemy.orm import Session


from app.db.database import SessionLocal
from app.models.meal_schedule import MealSchedule
from app.models.wallet import Wallet
from app.models.wallet_transaction import WalletTransaction


def process_today_meal():
    db:Session = SessionLocal()
    today = date.today()
    meals = db.query(MealSchedule).filter(MealSchedule.delivery_date==today,MealSchedule.status=="SCHEDULED").all()
    for meal in meals:
        wallet = db.query(Wallet).filter(Wallet.user_id == meal.user_id).first()
        if wallet.balance <meal.price:
            continue
        wallet.balance -= meal.price
        transaction = WalletTransaction(
            user_id = meal.user_id,
            amount = meal.price,
            transaction_type= "DEBIT",
            description = f"Payment for meal {meal.id} on {meal.delivery_date}"

        )
        db.add(transaction)
        meal.status = "DELIVERED"
    db.commit()
    db.close()


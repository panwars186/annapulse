from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.models.subscription_plan import SubscriptionPlan
from app.models.wallet import Wallet
from app.models.wallet_transaction import WalletTransaction


def deduct_daily_meal_cost(db:Session,subscription:Subscription):
    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == subscription.plan_id).first()
    wallet = db.query(Wallet).filter(Wallet.user_id == subscription.user_id).first()
    per_meal_cost = plan.price / plan.duration_days
    if wallet.balance< per_meal_cost:
        subscription.status = "PAUSED"
        return "Insufficient balance. Subscription paused."
    wallet.balance -= per_meal_cost
    transaction = WalletTransaction(wallet_id = wallet.id,amount = per_meal_cost,type = "DEBIT",
                                    descriptin = "Daily Meal deduction")
    db.add(transaction)
    db.commit()
    return "Meal Billed"

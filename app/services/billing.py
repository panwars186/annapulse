import logging

from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.models.subscription_plan import SubscriptionPlan
from app.models.wallet import Wallet
from app.models.wallet_transaction import WalletTransaction

logger = logging.getLogger(__name__)


def deduct_daily_meal_cost(db: Session, subscription: Subscription) -> str:
    try:
        plan = (
            db.query(SubscriptionPlan)
            .filter(SubscriptionPlan.id == subscription.plan_id)
            .first()
        )
        wallet = (
            db.query(Wallet)
            .filter(Wallet.user_id == subscription.user_id)
            .first()
        )
    except Exception:  # noqa: BLE001
        logger.exception(
            "Failed to load billing context for subscription_id=%s",
            subscription.id,
        )
        raise

    if not plan or not wallet:
        logger.warning(
            "Missing plan or wallet for subscription_id=%s (plan=%s, wallet=%s)",
            subscription.id,
            bool(plan),
            bool(wallet),
        )
        return "Billing skipped due to missing data."

    per_meal_cost = plan.price / plan.duration_days

    if wallet.balance < per_meal_cost:
        subscription.status = "PAUSED"
        logger.info(
            "Insufficient balance for user_id=%s, subscription_id=%s; pausing subscription",
            subscription.user_id,
            subscription.id,
        )
        return "Insufficient balance. Subscription paused."

    wallet.balance -= per_meal_cost
    transaction = WalletTransaction(
        wallet_id=wallet.id,
        amount=per_meal_cost,
        transaction_type="DEBIT",
        description="Daily meal deduction",
    )

    db.add(transaction)
    logger.info(
        "Successfully billed user_id=%s, subscription_id=%s, amount=%s",
        subscription.user_id,
        subscription.id,
        per_meal_cost,
    )
    return "Meal billed"


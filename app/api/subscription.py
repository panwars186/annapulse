import logging
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.deps import get_db
from app.models.subscription import Subscription
from app.models.subscription_plan import SubscriptionPlan
from app.schemas.subscription import SubscribePlan
from app.services.meal_generator import generate_meals

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])
logger = logging.getLogger(__name__)


@router.post("/")
def subscribe_plan(
    data: SubscribePlan,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        plan = (
            db.query(SubscriptionPlan)
            .filter(SubscriptionPlan.id == data.plan_id)
            .first()
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to load plan_id=%s", data.plan_id)
        raise HTTPException(status_code=500, detail="Failed to subscribe to plan") from exc

    if not plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")

    end_date = datetime.utcnow() + timedelta(days=plan.duration_days)
    subscription = Subscription(
        user_id=current_user.id,
        plan_id=plan.id,
        end_date=end_date,
    )

    try:
        db.add(subscription)
        db.commit()
        db.refresh(subscription)

        generate_meals(
            db,
            subscription,
            plan.meal_type,
            plan.duration_days,
        )
        db.commit()
    except Exception:  # noqa: BLE001
        logger.exception("Failed to create subscription for user_id=%s", current_user.id)
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create subscription")

    return subscription


@router.post("/pause")
def pause_subscription(
    pause_from: date,
    pause_to: date,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.user_id == current_user.id,
                Subscription.status == "ACTIVE",
            )
            .first()
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to pause subscription for user_id=%s", current_user.id)
        raise HTTPException(status_code=500, detail="Failed to pause subscription") from exc

    if not subscription:
        raise HTTPException(status_code=404, detail="Active Subscription not found")

    subscription.pause_from = pause_from
    subscription.pause_to = pause_to
    db.commit()

    return {"message": "Subscription paused successfully"}


@router.post("/resume")
def resume_subscription(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.user_id == current_user.id,
                Subscription.status == "ACTIVE",
            )
            .first()
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to resume subscription for user_id=%s", current_user.id)
        raise HTTPException(status_code=500, detail="Failed to resume subscription") from exc

    if not subscription:
        raise HTTPException(status_code=404, detail="Active Subscription not found")

    subscription.pause_from = None
    subscription.pause_to = None
    db.commit()

    return {"message": "Subscription resumed successfully"}

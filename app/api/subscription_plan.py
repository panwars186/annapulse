from typing import List
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.deps import get_db
from app.models.subscription_plan import SubscriptionPlan
from app.schemas.subscription_plan import SubscriptionPlanCreate, SubscriptionPlanResponse

router = APIRouter(prefix="/plans", tags=["Subscription Plans"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=SubscriptionPlanResponse)
def create_plan(
    plan: SubscriptionPlanCreate,
    db: Session = Depends(get_db),
):
    new_plan = SubscriptionPlan(**plan.dict())
    try:
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)
    except Exception:  # noqa: BLE001
        logger.exception("Failed to create subscription plan")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create subscription plan")

    return new_plan


@router.get("/", response_model=List[SubscriptionPlanResponse])
def list_plans(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return (
            db.query(SubscriptionPlan)
            .filter(SubscriptionPlan.is_active.is_(True))
            .all()
        )
    except Exception:  # noqa: BLE001
        logger.exception("Failed to list subscription plans for user_id=%s", current_user.id)
        raise HTTPException(status_code=500, detail="Failed to list subscription plans")

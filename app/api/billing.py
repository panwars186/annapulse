import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.subscription import Subscription
from app.services.billing import deduct_daily_meal_cost

router = APIRouter(prefix="/billing", tags=["Billing"])
logger = logging.getLogger(__name__)


@router.post("/run")
def run_billing(
    db: Session = Depends(get_db),
):
    try:
        subscriptions = (
            db.query(Subscription)
            .filter(Subscription.status == "ACTIVE")
            .all()
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to load subscriptions for billing")
        raise HTTPException(status_code=500, detail="Failed to run billing") from exc

    results = []
    try:
        for sub in subscriptions:
            result = deduct_daily_meal_cost(db, sub)
            results.append(result)

        db.commit()
    except Exception:  # noqa: BLE001
        logger.exception("Error while running billing job via API")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to run billing")

    return {"Billing Results": results}

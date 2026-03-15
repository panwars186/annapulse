from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.subscription import Subscription
from app.services.billing import deduct_daily_meal_cost

router = APIRouter(prefix="/billing",tags=["Billing"])

@router.post("/run")
def run_billing(
    db:Session = Depends(get_db)):
    subscriptions = db.query(Subscription).filter(Subscription.status == "ACTIVE").all()
    results = []

    for sub in subscriptions:
        result = deduct_daily_meal_cost(db,sub)
        results.append(result)
    return {"Billing Results":results}
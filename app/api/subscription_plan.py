from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.deps import get_db
from app.models.subscription_plan import SubscriptionPlan
from app.schemas.subscription_plan import SubscriptionPlanCreate, SubscriptionPlanResponse

router = APIRouter(prefix="/plans",tags=["Subscription Plans"])

@router.post("/",response_model=SubscriptionPlanResponse)
def create_plan(
    plan:SubscriptionPlanCreate,
    db:Session = Depends(get_db)):
    new_plan = SubscriptionPlan(**plan.dict())
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan

@router.get("/",response_model=List[SubscriptionPlanResponse])
def list_plans(
    db:Session = Depends(get_db),
    current_user = Depends(get_current_user)):
    return db.query(SubscriptionPlan).filter(SubscriptionPlan.is_active==True).all()


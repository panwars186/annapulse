from datetime import datetime, timedelta, date

from aiohttp.abc import HTTPException
from fastapi import APIRouter, Depends
from onnxruntime.capi.onnxruntime_inference_collection import Session
from sympy.polys.densetools import dmp_eval_tail

from app.models.subscription import Subscription
from app.core.dependencies import get_current_user
from app.db.deps import get_db
from app.models.subscription_plan import SubscriptionPlan
from app.schemas.subscription import SubscribePlan
from app.services.meal_generator import generate_meals
router = APIRouter(prefix="/subscriptions",tags=["Subscriptions"])

@router.post("/")
def subscribe_plan(
    data:SubscribePlan,
    db:Session=Depends(get_db),
    current_user = Depends(get_current_user)):
    plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.id == data.plan_id).first()
    end_date = datetime.utcnow() + timedelta(days=plan.duration_days)
    subscription = Subscription(
    user_id = current_user.id,
    plan_id = plan.id,
    end_date=end_date
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    generate_meals(
    db,
    subscription,
    plan.meal_type,
    plan.duration_days
    )

    return subscription

@router.post("/pause")
def pause_subsription(
    pause_from:date,
    pause_to:date,
    db:Session=Depends(get_db),
    current_user = Depends(get_current_user)):
    subscription = db.query(Subscription).filter(Subscription.user_id==current_user.id,
                   Subscription.status=="ACTIVE").first()
    if not subscription:
        raise HTTPException(status_code=404,detail="Active Subscription not found")
    subscription.pause_from = pause_from
    subscription.pause_to = pause_to
    db.commit()
    return {"message":"Subscription paused successfully"}

@router.post("/resume")
def resume_subscription(
    db:Session =Depends(get_db),
    current_user = Depends(get_current_user)):
    subscription = db.query(Subscription).filter(Subscription.user_id==current_user,
                    Subscription.status=="ACTIVE").first()
    if not subscription:
        raise HTTPException(status_code = 404, detail="Active Subscription not found")
    subscription.pause_from= None
    subscription.pause_to = None
    db.commit()
    return {"message":"Subscription resumed successfully"}
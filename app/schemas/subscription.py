from pydantic import BaseModel
from datetime import datetime

class SubscribePlan(BaseModel):
    plan_id:int

class SubscriptionResponse(BaseModel):
    id:int
    user_id:int
    plan_id:int
    start_date:datetime
    end_date:datetime
    status:str

    class Config:
        from_attributes = True
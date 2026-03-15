from pydantic import BaseModel

class SubscriptionPlanCreate(BaseModel):
    name:str
    duration_days:int
    meal_types:str
    price:float


class SubscriptionPlanResponse(BaseModel):
    id:int
    name:str
    duration_days:int
    meal_type:str
    price:float

    class Config:
        from_attributes = True

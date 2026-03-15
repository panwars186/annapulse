from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    meal_id:int
    rating:int
    comment:str


class FeedbackResponse(BaseModel):
    id:int
    meal_id:int
    rating:int
    comment:str

    class Config:
        from_attributes = True

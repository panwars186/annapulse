from pydantic import BaseModel

class MenuCreate(BaseModel):
    day_of_week:str
    meal_type:str
    dish_name:str

class MenuResponse(BaseModel):
    id:int
    day_of_week:str
    meal_type:str
    dish_name:str

    class Config:
        from_attributes = True
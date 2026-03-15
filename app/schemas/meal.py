from pydantic import BaseModel
from datetime import datetime

class SkilMealRequest(BaseModel):
    schedule_id:int
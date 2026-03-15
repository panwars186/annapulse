from datetime import datetime


from sqlalchemy import Column, Integer, String, ForeignKey,DateTime

from app.db.database import Base


class MealSchedule(Base):
    __tablename__ = "meal_schedules"

    id = Column(Integer, primary_key = True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    meal_type = Column(String)
    delivery_date = Column(DateTime)
    status = Column(String, default= "SCHEDULED")




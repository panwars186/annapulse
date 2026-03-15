from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from app.db.database import Base

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(Integer,primary_key=True,index = True)
    name = Column(String, nullable=False)
    duration_days = Column(Integer, nullable=False)
    meal_types = Column(String,nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)


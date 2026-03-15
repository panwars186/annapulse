from datetime import datetime


from sqlalchemy import Column, Integer, ForeignKey,DateTime,String

from app.db.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer,primary_key=True,index = True)
    user_id = Column(Integer,ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"))

    start_date = Column(DateTime,default=datetime.utcnow)
    end_date = Column(DateTime)
    status = Column(String, default="ACTIVE")
    pause_from = Column(DateTime,nullable = True)
    pause_to = Column(DateTime,nullable=True)


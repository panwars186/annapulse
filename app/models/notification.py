from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.db.database import Base


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer,primary_key = True,index = True)
    user_id = Column(Integer)
    title = Column(String)
    message = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime,default = datetime.utcnow)



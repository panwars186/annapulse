from sqlalchemy import Column,Integer,String,DateTime,Boolean
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    dob = Column(String, nullable=True)
    address = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    area = Column(String)
    created_at = Column(DateTime(timezone=True),server_default = func.now())
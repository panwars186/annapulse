
from sqlalchemy import Column, Integer, String,DateTime
from sqlalchemy.sql import func
from app.db.database import Base


class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer,primary_key=True,index=True)
    phone_number = Column(String, index = True)
    otp_code = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

from sqlalchemy import Integer, ForeignKey, Column, Float

from app.db.database import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    balance = Column(Float,default=0)

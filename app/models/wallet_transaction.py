from datetime import datetime, timezone

from sqlalchemy import Column, Integer, ForeignKey, Float, String,DateTime

from app.db.database import Base


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(Integer,primary_key=True,index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"))
    amount = Column(Float)
    type = Column(String)  # "CREDIT" or "DEBIT"
    description = Column(String)

    created_at = Column(DateTime,default=datetime.now(timezone.utc))


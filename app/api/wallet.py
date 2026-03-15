from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session


from app.core.dependencies import get_current_user
from app.db.deps import get_db
from app.models.wallet import Wallet
from app.schemas.wallet import AddMoneyRequest

router = APIRouter(prefix="/wallet",tags=["Wallet"])

@router.get("/")
def get_wallet(
    db:Session= Depends(get_db),
    current_user = Depends(get_current_user)):
    wallet = db.query(Wallet).filter(Wallet.user_id== current_user.id).first()
    return wallet

@router.post("/add")
def add_money(
    data:AddMoneyRequest,
    db:Session =Depends(get_db),
    current_user = Depends(get_current_user)):
    wallet = db.query(Wallet).filter(Wallet.user_id==current_user.id).first()
    wallet.balance += data.amount

    db.commit()
    return {"message":"Money added successfully","balance":wallet.balance}

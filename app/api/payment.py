import razorpay
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.models.wallet import Wallet
from app.core.config import RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET
from app.core.dependencies import get_current_user
from app.db.deps import get_db
from app.models.wallet_transaction import WalletTransaction

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/create_order")
def create_order(amount:float):
    order= client.order.create({
        "amount": amount*100,
        "currency": "INR",
        "payment_capture": 1
    })

    return order

@router.post("/verify_payment")
def verify_payment(
    razorpay_order_id:str,
    razorpay_payment_id:str,
    razorpay_signature:str,
    amount :float,
    db:Session =Depends(get_db),
    current_user = Depends(get_current_user)):
    try:
        client.utility.verify_payment_signature({
        "razorpay_order_id": razorpay_order_id,
        "razorpay_payment_id": razorpay_payment_id,
        "razorpay_signature": razorpay_signature
        })

    except:
        raise HTTPException(status_code = 400,detail="Payment verification failed")
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        raise HTTPException(status_code=404,detail="Wallet not found")
    wallet.balance +=amount
    transaction = WalletTransaction(
        user_id = current_user.id,
        amount = amount,
        transaction_type = "CREDIT",
        description = "Wallet top-up via Razorpay"
    )
    db.add(transaction)
    db.commit()
    return {
        "message":"Payment verified and wallet updated successfully",
        "balance": wallet.balance
    }
import logging

import razorpay
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
from app.core.dependencies import get_current_user
from app.db.deps import get_db
from app.models.wallet import Wallet
from app.models.wallet_transaction import WalletTransaction

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

router = APIRouter(prefix="/payment", tags=["Payment"])
logger = logging.getLogger(__name__)


@router.post("/create_order")
def create_order(amount: float):
    try:
        order = client.order.create(
            {
                "amount": int(amount * 100),
                "currency": "INR",
                "payment_capture": 1,
            }
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to create Razorpay order for amount=%s", amount)
        raise HTTPException(status_code=500, detail="Failed to create payment order") from exc

    return order


@router.post("/verify_payment")
def verify_payment(
    razorpay_order_id: str,
    razorpay_payment_id: str,
    razorpay_signature: str,
    amount: float,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }
        )
    except Exception:  # noqa: BLE001
        logger.warning(
            "Payment verification failed for order_id=%s, payment_id=%s",
            razorpay_order_id,
            razorpay_payment_id,
        )
        raise HTTPException(status_code=400, detail="Payment verification failed")

    try:
        wallet = (
            db.query(Wallet)
            .filter(Wallet.user_id == current_user.id)
            .first()
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to load wallet for user_id=%s", current_user.id)
        raise HTTPException(status_code=500, detail="Failed to verify payment") from exc

    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    try:
        wallet.balance += amount
        transaction = WalletTransaction(
            user_id=current_user.id,
            amount=amount,
            transaction_type="CREDIT",
            description="Wallet top-up via Razorpay",
        )
        db.add(transaction)
        db.commit()
    except Exception:  # noqa: BLE001
        logger.exception("Failed to update wallet after payment for user_id=%s", current_user.id)
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update wallet after payment")

    return {
        "message": "Payment verified and wallet updated successfully",
        "balance": wallet.balance,
    }

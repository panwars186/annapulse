import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.deps import get_db
from app.models.wallet import Wallet
from app.schemas.wallet import AddMoneyRequest

router = APIRouter(prefix="/wallet", tags=["Wallet"])
logger = logging.getLogger(__name__)


@router.get("/")
def get_wallet(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        wallet = (
            db.query(Wallet)
            .filter(Wallet.user_id == current_user.id)
            .first()
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to fetch wallet for user_id=%s", current_user.id)
        raise HTTPException(status_code=500, detail="Failed to fetch wallet") from exc

    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    return wallet


@router.post("/add")
def add_money(
    data: AddMoneyRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        wallet = (
            db.query(Wallet)
            .filter(Wallet.user_id == current_user.id)
            .first()
        )
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")

        wallet.balance += data.amount
        db.commit()
    except HTTPException:
        # Re-raise HTTP errors directly.
        raise
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to add money for user_id=%s", current_user.id)
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to add money") from exc

    return {"message": "Money added successfully", "balance": wallet.balance}


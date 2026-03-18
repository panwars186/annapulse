import logging
from random import randint

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.deps import get_db
from app.models.otp import OTP
from app.models.user import User
from app.schemas.auth import OTPVerify, PhoneRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)


@router.post("/request-otp")
def request_otp(data: PhoneRequest, db: Session = Depends(get_db)):
    otp_code = str(randint(100000, 999999))

    try:
        otp = OTP(phone_number=data.phone_number, otp_code=otp_code)
        db.add(otp)
        db.commit()
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to create OTP for %s", data.phone_number)
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create OTP") from exc

    # In production, you would not return the OTP in the response.
    return {"message": "OTP generated", "otp": otp_code}


@router.post("/verify-otp", response_model=TokenResponse)
def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):
    try:
        otp_record = (
            db.query(OTP)
            .filter(
                OTP.phone_number == data.phone_number,
                OTP.otp_code == data.otp_code,
            )
            .order_by(OTP.created_at.desc())
            .first()
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to verify OTP for %s", data.phone_number)
        raise HTTPException(status_code=500, detail="Failed to verify OTP") from exc

    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    try:
        user = db.query(User).filter(User.phone_number == data.phone_number).first()
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to load user for %s", data.phone_number)
        raise HTTPException(status_code=500, detail="Failed to verify user") from exc

    if not user:
        raise HTTPException(status_code=404, detail="User not registered")

    token = create_access_token({"sub": user.phone_number})
    return {"access_token": token}

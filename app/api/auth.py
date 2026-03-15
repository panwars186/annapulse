from random import random ,randint

from aiohttp.abc import HTTPException
from fastapi import APIRouter
from fastapi.params import Depends
from langchain_community.llms.databricks import get_default_host
from onnxruntime.capi.onnxruntime_inference_collection import Session

from app.core.security import create_access_token
from app.db.deps import get_db
from app.models.otp import OTP
from app.models.user import User
from app.schemas.auth import PhoneRequest, OTPVerify, TokenResponse

router = APIRouter(prefix="/auth",tags = ["Authentication"])

@router.post("/request-otp")
def request_otp(data:PhoneRequest,db:Session = Depends(get_db)):
    otp_code = str(randint(100000,999999))
    otp = OTP(phone_number = data.phone_number,otp_code=otp_code)
    db.add(otp)
    db.commit()

    return {"message":"OTP generated","otp":otp_code}

@router.post("/verify-otp",response_model=TokenResponse)
def verify_otp(data:OTPVerify,db:Session=Depends(get_db)):
    otp_record = (db.query(OTP).filter(OTP.phone_number==data.phone_number,OTP.otp_code==data.otp_code).
                  order_by(OTP.created_at.desc()).first())

    if not otp_record:
        raise HTTPException(status_code=400,detail="Invalid OTP")
    user = db.query(User).filter(User.phone_number == data.phone_number).first()

    if not user:
        raise HTTPException(status_code=404,detail="user not registered")
    token = create_access_token({"sub":user.phone_number})
    return {"access_token":token}



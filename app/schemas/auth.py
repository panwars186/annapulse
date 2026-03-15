from pydantic import BaseModel

class PhoneRequest(BaseModel):

    phone_number:str

class OTPVerify(BaseModel):
    phone_number:str
    otp_code:str

class TokenResponse(BaseModel):
    access_token:str
    token_type:str = "bearer"
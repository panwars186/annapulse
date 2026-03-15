from pydantic import BaseModel

class AddMoneyRequest(BaseModel):
    amount:float

class WalletResponse(BaseModel):
    balance:float

    class Config:
        from_attributes = True
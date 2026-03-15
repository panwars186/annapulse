from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name:str
    phone_number:str=Field(...,min_length=10,max_length=20)
    dob :str |None =None
    address:str|None =None

class UserResponse(BaseModel):
    id:int
    name:str
    phone_number:str
    dob :str |None =None
    address:str|None =None


    class Config:
        from_attributes = True
from pydantic import BaseModel, EmailStr
from datetime import datetime
from decimal import Decimal
from typing import Optional

#USER
class UserCreate(BaseModel):
    username:str
    email:EmailStr
    password:str
    
class UserResponse(BaseModel):
    id:int
    username:str
    email:EmailStr
    created_at:datetime
    
    class Config:
        orm_mode = True
        
#ACCOUNT
class AccountCreate(BaseModel):
    account_numbers:str
    balance:Optional[Decimal] = Decimal("0.00")
    
class AccountResponse(BaseModel):
    id:int
    account_numbers:str
    balance:Decimal
    user_id:int
    created_at:datetime
    
    class Config:
        orm_mode = True
    
#TRANSACTION
class TransactionCreate(BaseModel):
    type:str # deposit | withDraw | transfer
    amount:Decimal
    account_id:int
    related_account_id:Optional[int] = None
    description:Optional[str] = None
    
class TransactionResponse(BaseModel):
    id:int
    type:str
    amount:Decimal
    date:datetime
    account_id:int
    related_account_id:Optional[int] = None
    description:Optional[str] = None
    
    class Config:
        orm_mode = True 
      
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class TierEnum(str, Enum):
    free = "free"
    premium = "premium"

class UserBase(BaseModel):
    username: str
    email: str
    tier: TierEnum = TierEnum.free

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: str

class PasswordResetRequest(BaseModel):
    email: str

class PasswordReset(BaseModel):
    token: str
    new_password: str

from pydantic import BaseModel
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

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

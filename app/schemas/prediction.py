from pydantic import BaseModel
from typing import Optional
from enum import Enum

class ThumbEnum(str, Enum):
    up = "up"
    down = "down"

class PredictionBase(BaseModel):
    cityname: str
    country: str
    rate: int
    reason: str
    thumb: Optional[ThumbEnum] = None

class PredictionCreate(PredictionBase):
    user_id: int

class Prediction(PredictionBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True 
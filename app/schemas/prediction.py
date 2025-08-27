from pydantic import BaseModel, Field
from datetime import date
from typing import List

class CityPrediction(BaseModel):
    city: str
    rate: int = Field(..., ge=1, le=100)
    reason: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class PredictionRequest(BaseModel):
    birthday: date
    country: str

class PredictionResponse(BaseModel):
    four_pillars: str
    predictions: List[CityPrediction] 
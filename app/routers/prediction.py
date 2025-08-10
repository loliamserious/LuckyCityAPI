from fastapi import APIRouter, HTTPException
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.deepseek_client import get_predictions

router = APIRouter(prefix="/predictions", tags=["predictions"])

@router.post("/", response_model=PredictionResponse)
async def predict_cities(request: PredictionRequest):
    try:
        # Get predictions in a single API call
        result = await get_predictions(request.birthday.isoformat(), request.country)
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting predictions: {str(e)}"
        ) 
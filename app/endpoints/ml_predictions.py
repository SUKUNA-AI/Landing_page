from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import ml_predictions
from ..dao import MLPredictionDAO
from typing import List

router = APIRouter(prefix="/ml_predictions", tags=["ml_predictions"])

@router.post("/", response_model=ml_predictions.MLPredictionResponse)
async def create_ml_prediction(prediction_data: ml_predictions.MLPredictionCreate, db: AsyncSession = Depends(get_db)):
    """Создает новое предсказание машинного обучения."""
    return await MLPredictionDAO.create(db, prediction_data.dict())

@router.get("/{message_id}", response_model=List[ml_predictions.MLPredictionResponse])
async def get_ml_predictions(message_id: int, db: AsyncSession = Depends(get_db)):
    """Получает предсказания ML по message_id."""
    query = (
        ml_predictions.MLPrediction.__table__.select()
        .where(ml_predictions.MLPrediction.message_id == message_id)
    )
    result = await db.execute(query)
    predictions = result.fetchall()
    if not predictions:
        raise HTTPException(status_code=404, detail="ML predictions not found")
    return predictions
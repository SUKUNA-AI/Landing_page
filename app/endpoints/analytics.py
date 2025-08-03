from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import analytics
from ..dao import AnalyticsDAO
from typing import List

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.post("/", response_model=analytics.AnalyticsResponse)
async def create_analytics(analytics_data: analytics.AnalyticsCreate, db: AsyncSession = Depends(get_db)):
    """Создает новую запись аналитики."""
    return await AnalyticsDAO.create(db, analytics_data.dict())

@router.get("/", response_model=List[analytics.AnalyticsResponse])
async def get_analytics(db: AsyncSession = Depends(get_db)):
    """Получает все записи аналитики."""
    analytics_list = await AnalyticsDAO.get_all(db)
    if not analytics_list:
        raise HTTPException(status_code=404, detail="Analytics records not found")
    return analytics_list

@router.get("/{analytics_id}", response_model=analytics.AnalyticsResponse)
async def get_analytics_by_id(analytics_id: int, db: AsyncSession = Depends(get_db)):
    """Получает запись аналитики по ID."""
    analytics_record = await AnalyticsDAO.get_by_id(db, analytics_id)
    if not analytics_record:
        raise HTTPException(status_code=404, detail="Analytics record not found")
    return analytics_record
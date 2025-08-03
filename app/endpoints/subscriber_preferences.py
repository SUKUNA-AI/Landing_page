from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import subscriber_preferences
from ..dao import SubscriberPreferenceDAO
from typing import List

router = APIRouter(prefix="/subscriber_preferences", tags=["subscriber_preferences"])

@router.post("/", response_model=subscriber_preferences.SubscriberPreferenceResponse)
async def create_subscriber_preference(pref_data: subscriber_preferences.SubscriberPreferenceCreate, db: AsyncSession = Depends(get_db)):
    """Создает новое предпочтение подписчика."""
    return await SubscriberPreferenceDAO.create(db, pref_data.dict())

@router.get("/{telegram_user_id}", response_model=List[subscriber_preferences.SubscriberPreferenceResponse])
async def get_subscriber_preferences(telegram_user_id: str, db: AsyncSession = Depends(get_db)):
    """Получает предпочтения подписчика по telegram_user_id."""
    query = (
        subscriber_preferences.SubscriberPreference.__table__.select()
        .where(subscriber_preferences.SubscriberPreference.telegram_user_id == telegram_user_id)
    )
    result = await db.execute(query)
    preferences = result.fetchall()
    if not preferences:
        raise HTTPException(status_code=404, detail="Subscriber preferences not found")
    return preferences

@router.put("/{preference_id}", response_model=subscriber_preferences.SubscriberPreferenceResponse)
async def update_subscriber_preference(preference_id: int, pref_data: subscriber_preferences.SubscriberPreferenceUpdate, db: AsyncSession = Depends(get_db)):
    """Обновляет данные предпочтения подписчика."""
    preference = await SubscriberPreferenceDAO.get_by_id(db, preference_id)
    if not preference:
        raise HTTPException(status_code=404, detail="Subscriber preference not found")
    update_data = pref_data.dict(exclude_unset=True)
    query = (
        subscriber_preferences.SubscriberPreference.__table__.update()
        .where(subscriber_preferences.SubscriberPreference.id == preference_id)
        .values(**update_data)
        .returning(subscriber_preferences.SubscriberPreference.__table__)
    )
    result = await db.execute(query)
    await db.commit()
    updated_preference = result.first()
    if not updated_preference:
        raise HTTPException(status_code=404, detail="Subscriber preference not found after update")
    return updated_preference

@router.delete("/{preference_id}", status_code=204)
async def delete_subscriber_preference(preference_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет предпочтение подписчика по ID."""
    preference = await SubscriberPreferenceDAO.get_by_id(db, preference_id)
    if not preference:
        raise HTTPException(status_code=404, detail="Subscriber preference not found")
    query = subscriber_preferences.SubscriberPreference.__table__.delete().where(subscriber_preferences.SubscriberPreference.id == preference_id)
    await db.execute(query)
    await db.commit()
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import telegram_subscribers
from ..dao import TelegramSubscriberDAO

router = APIRouter(prefix="/telegram_subscribers", tags=["telegram_subscribers"])

@router.post("/", response_model=telegram_subscribers.TelegramSubscriberResponse)
async def create_telegram_subscriber(subscriber_data: telegram_subscribers.TelegramSubscriberCreate, db: AsyncSession = Depends(get_db)):
    """Создает нового подписчика Telegram."""
    return await TelegramSubscriberDAO.create(db, subscriber_data.dict())

@router.get("/{telegram_user_id}", response_model=telegram_subscribers.TelegramSubscriberResponse)
async def get_telegram_subscriber(telegram_user_id: str, db: AsyncSession = Depends(get_db)):
    """Получает подписчика Telegram по его ID."""
    query = (
        telegram_subscribers.TelegramSubscriber.__table__.select()
        .where(telegram_subscribers.TelegramSubscriber.telegram_user_id == telegram_user_id)
    )
    result = await db.execute(query)
    subscriber = result.first()
    if not subscriber:
        raise HTTPException(status_code=404, detail="Telegram subscriber not found")
    return subscriber

@router.delete("/{telegram_user_id}", status_code=204)
async def delete_telegram_subscriber(telegram_user_id: str, db: AsyncSession = Depends(get_db)):
    """Удаляет подписчика Telegram по ID."""
    query = (
        telegram_subscribers.TelegramSubscriber.__table__.delete()
        .where(telegram_subscribers.TelegramSubscriber.telegram_user_id == telegram_user_id)
    )
    result = await db.execute(query)
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Telegram subscriber not found")
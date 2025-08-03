from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import social_media
from ..dao import SocialMediaDAO
from typing import List

router = APIRouter(prefix="/social_media", tags=["social_media"])

@router.post("/", response_model=social_media.SocialMediaResponse)
async def create_social_media(social_data: social_media.SocialMediaCreate, db: AsyncSession = Depends(get_db)):
    """Создает новую запись о социальной сети."""
    return await SocialMediaDAO.create(db, social_data.dict())

@router.get("/{user_id}", response_model=List[social_media.SocialMediaResponse])
async def get_social_media(user_id: int, db: AsyncSession = Depends(get_db)):
    """Получает записи о социальных сетях пользователя по его ID."""
    social_media_list = await SocialMediaDAO.get_by_user_id(db, user_id)
    if not social_media_list:
        raise HTTPException(status_code=404, detail="Social media not found")
    return social_media_list

@router.put("/{social_id}", response_model=social_media.SocialMediaResponse)
async def update_social_media(social_id: int, social_data: social_media.SocialMediaUpdate, db: AsyncSession = Depends(get_db)):
    """Обновляет данные записи о социальной сети."""
    social = await SocialMediaDAO.get_by_id(db, social_id)
    if not social:
        raise HTTPException(status_code=404, detail="Social media not found")
    update_data = social_data.dict(exclude_unset=True)
    query = (
        social_media.SocialMedia.__table__.update()
        .where(social_media.SocialMedia.id == social_id)
        .values(**update_data)
        .returning(social_media.SocialMedia.__table__)
    )
    result = await db.execute(query)
    await db.commit()
    updated_social = result.first()
    if not updated_social:
        raise HTTPException(status_code=404, detail="Social media not found after update")
    return updated_social

@router.delete("/{social_id}", status_code=204)
async def delete_social_media(social_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет запись о социальной сети по ID."""
    social = await SocialMediaDAO.get_by_id(db, social_id)
    if not social:
        raise HTTPException(status_code=404, detail="Social media not found")
    query = social_media.SocialMedia.__table__.delete().where(social_media.SocialMedia.id == social_id)
    await db.execute(query)
    await db.commit()
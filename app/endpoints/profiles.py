from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import profile
from ..dao import ProfileDAO
from typing import List

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.post("/", response_model=profile.ProfileResponse)
async def create_profile(profile_data: profile.ProfileCreate, db: AsyncSession = Depends(get_db)):
    """Создает новый профиль пользователя."""
    return await ProfileDAO.create(db, profile_data.dict())

@router.get("/{user_id}", response_model=List[profile.ProfileResponse])
async def get_profiles(user_id: int, db: AsyncSession = Depends(get_db)):
    """Получает профили пользователя по его ID."""
    profiles = await ProfileDAO.get_by_user_id(db, user_id)
    if not profiles:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profiles

@router.put("/{profile_id}", response_model=profile.ProfileResponse)
async def update_profile(profile_id: int, profile_data: profile.ProfileUpdate, db: AsyncSession = Depends(get_db)):
    """Обновляет данные профиля."""
    profile = await ProfileDAO.get_by_id(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    update_data = profile_data.dict(exclude_unset=True)
    query = (
        profile.Profile.__table__.update()
        .where(profile.Profile.id == profile_id)
        .values(**update_data)
        .returning(profile.Profile.__table__)
    )
    result = await db.execute(query)
    await db.commit()
    updated_profile = result.first()
    if not updated_profile:
        raise HTTPException(status_code=404, detail="Profile not found after update")
    return updated_profile

@router.delete("/{profile_id}", status_code=204)
async def delete_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет профиль по ID."""
    profile = await ProfileDAO.get_by_id(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    query = profile.Profile.__table__.delete().where(profile.Profile.id == profile_id)
    await db.execute(query)
    await db.commit()
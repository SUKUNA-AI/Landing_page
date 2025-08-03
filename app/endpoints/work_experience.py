from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import work_experience
from ..dao import WorkExperienceDAO
from typing import List

router = APIRouter(prefix="/work_experience", tags=["work_experience"])

@router.post("/", response_model=work_experience.WorkExperienceResponse)
async def create_work_experience(work_data: work_experience.WorkExperienceCreate, db: AsyncSession = Depends(get_db)):
    """Создает новую запись об опыте работы."""
    return await WorkExperienceDAO.create(db, work_data.dict())

@router.get("/{user_id}", response_model=List[work_experience.WorkExperienceResponse])
async def get_work_experience(user_id: int, db: AsyncSession = Depends(get_db)):
    """Получает записи об опыте работы пользователя по его ID."""
    work_experience_list = await WorkExperienceDAO.get_by_user_id(db, user_id)
    if not work_experience_list:
        raise HTTPException(status_code=404, detail="Work experience records not found")
    return work_experience_list

@router.put("/{work_id}", response_model=work_experience.WorkExperienceResponse)
async def update_work_experience(work_id: int, work_data: work_experience.WorkExperienceUpdate, db: AsyncSession = Depends(get_db)):
    """Обновляет данные записи об опыте работы."""
    work_experience = await WorkExperienceDAO.get_by_id(db, work_id)
    if not work_experience:
        raise HTTPException(status_code=404, detail="Work experience record not found")
    update_data = work_data.dict(exclude_unset=True)
    query = (
        work_experience.WorkExperience.__table__.update()
        .where(work_experience.WorkExperience.id == work_id)
        .values(**update_data)
        .returning(work_experience.WorkExperience.__table__)
    )
    result = await db.execute(query)
    await db.commit()
    updated_work_experience = result.first()
    if not updated_work_experience:
        raise HTTPException(status_code=404, detail="Work experience record not found after update")
    return updated_work_experience

@router.delete("/{work_id}", status_code=204)
async def delete_work_experience(work_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет запись об опыте работы по ID."""
    work_experience = await WorkExperienceDAO.get_by_id(db, work_id)
    if not work_experience:
        raise HTTPException(status_code=404, detail="Work experience record not found")
    query = work_experience.WorkExperience.__table__.delete().where(work_experience.WorkExperience.id == work_id)
    await db.execute(query)
    await db.commit()
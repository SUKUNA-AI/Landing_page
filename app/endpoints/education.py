from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import education
from ..dao import EducationDAO
from typing import List

router = APIRouter(prefix="/education", tags=["education"])

@router.post("/", response_model=education.EducationResponse)
async def create_education(edu_data: education.EducationCreate, db: AsyncSession = Depends(get_db)):
    """Создает новую запись об образовании."""
    return await EducationDAO.create(db, edu_data.dict())

@router.get("/{user_id}", response_model=List[education.EducationResponse])
async def get_education(user_id: int, db: AsyncSession = Depends(get_db)):
    """Получает записи об образовании пользователя по его ID."""
    education_list = await EducationDAO.get_by_user_id(db, user_id)
    if not education_list:
        raise HTTPException(status_code=404, detail="Education records not found")
    return education_list

@router.put("/{education_id}", response_model=education.EducationResponse)
async def update_education(education_id: int, edu_data: education.EducationUpdate, db: AsyncSession = Depends(get_db)):
    """Обновляет данные записи об образовании."""
    education = await EducationDAO.get_by_id(db, education_id)
    if not education:
        raise HTTPException(status_code=404, detail="Education record not found")
    update_data = edu_data.dict(exclude_unset=True)
    query = (
        education.Education.__table__.update()
        .where(education.Education.id == education_id)
        .values(**update_data)
        .returning(education.Education.__table__)
    )
    result = await db.execute(query)
    await db.commit()
    updated_education = result.first()
    if not updated_education:
        raise HTTPException(status_code=404, detail="Education record not found after update")
    return updated_education

@router.delete("/{education_id}", status_code=204)
async def delete_education(education_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет запись об образовании по ID."""
    education = await EducationDAO.get_by_id(db, education_id)
    if not education:
        raise HTTPException(status_code=404, detail="Education record not found")
    query = education.Education.__table__.delete().where(education.Education.id == education_id)
    await db.execute(query)
    await db.commit()
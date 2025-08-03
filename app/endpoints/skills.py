from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import skills
from ..dao import SkillDAO
from typing import List

router = APIRouter(prefix="/skills", tags=["skills"])

@router.post("/", response_model=skills.SkillResponse)
async def create_skill(skill_data: skills.SkillCreate, db: AsyncSession = Depends(get_db)):
    """Создает новый навык пользователя."""
    return await SkillDAO.create(db, skill_data.dict())

@router.get("/{user_id}", response_model=List[skills.SkillResponse])
async def get_skills(user_id: int, db: AsyncSession = Depends(get_db)):
    """Получает навыки пользователя по его ID."""
    skills_list = await SkillDAO.get_by_user_id(db, user_id)
    if not skills_list:
        raise HTTPException(status_code=404, detail="Skills not found")
    return skills_list

@router.put("/{skill_id}", response_model=skills.SkillResponse)
async def update_skill(skill_id: int, skill_data: skills.SkillUpdate, db: AsyncSession = Depends(get_db)):
    """Обновляет данные навыка."""
    skill = await SkillDAO.get_by_id(db, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    update_data = skill_data.dict(exclude_unset=True)
    query = (
        skills.Skill.__table__.update()
        .where(skills.Skill.id == skill_id)
        .values(**update_data)
        .returning(skills.Skill.__table__)
    )
    result = await db.execute(query)
    await db.commit()
    updated_skill = result.first()
    if not updated_skill:
        raise HTTPException(status_code=404, detail="Skill not found after update")
    return updated_skill

@router.delete("/{skill_id}", status_code=204)
async def delete_skill(skill_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет навык по ID."""
    skill = await SkillDAO.get_by_id(db, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    query = skills.Skill.__table__.delete().where(skills.Skill.id == skill_id)
    await db.execute(query)
    await db.commit()
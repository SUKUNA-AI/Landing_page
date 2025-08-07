from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import projects
from ..dao.models_dao import ProjectDAO
from ..auth import get_current_user
from aiogram import Bot
from ..config import settings
from typing import List

router = APIRouter(prefix="/projects", tags=["projects"])

# Инициализация бота
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

@router.post("/", response_model=projects.ProjectResponse)
async def create_project(
    project_data: projects.ProjectCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Создает новый проект пользователя."""
    return await ProjectDAO.create(db, project_data.dict(), bot=bot)

@router.get("/{user_id}", response_model=List[projects.ProjectResponse])
async def get_projects(user_id: int, db: AsyncSession = Depends(get_db)):
    """Получает проекты пользователя по его ID."""
    projects_list = await ProjectDAO.get_by_user_id(db, user_id)
    if not projects_list:
        raise HTTPException(status_code=404, detail="Projects not found")
    return projects_list

@router.put("/{project_id}", response_model=projects.ProjectResponse)
async def update_project(
    project_id: int,
    project_data: projects.ProjectUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновляет данные проекта."""
    return await ProjectDAO.update(db, project_id, project_data.dict(exclude_unset=True), bot=bot)

@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: int, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Удаляет проект по ID."""
    project = await ProjectDAO.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    query = projects.Project.__table__.delete().where(projects.Project.id == project_id)
    await db.execute(query)
    await db.commit()
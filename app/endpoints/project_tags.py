from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import project_tags
from ..dao import ProjectTagDAO

router = APIRouter(prefix="/project_tags", tags=["project_tags"])

@router.post("/", response_model=project_tags.ProjectTagResponse)
async def create_project_tag(project_tag_data: project_tags.ProjectTagCreate, db: AsyncSession = Depends(get_db)):
    """Создает связь между проектом и тегом."""
    return await ProjectTagDAO.create(db, project_tag_data.dict())

@router.delete("/{project_id}/{tag_id}", status_code=204)
async def delete_project_tag(project_id: int, tag_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет связь между проектом и тегом."""
    query = (
        project_tags.ProjectTag.__table__.delete()
        .where(project_tags.ProjectTag.project_id == project_id)
        .where(project_tags.ProjectTag.tag_id == tag_id)
    )
    result = await db.execute(query)
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="ProjectTag not found")
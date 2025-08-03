from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas import tasks
from ..dao import TaskDAO
from typing import List

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=tasks.TaskResponse)
async def create_task(task_data: tasks.TaskCreate, db: AsyncSession = Depends(get_db)):
    """Создает новую задачу."""
    return await TaskDAO.create(db, task_data.dict())

@router.get("/{user_id}", response_model=List[tasks.TaskResponse])
async def get_tasks(user_id: int, db: AsyncSession = Depends(get_db)):
    """Получает задачи пользователя по его ID."""
    tasks_list = await TaskDAO.get_by_user_id(db, user_id)
    if not tasks_list:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return tasks_list

@router.get("/task/{task_id}", response_model=tasks.TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """Получает задачу по ID."""
    task = await TaskDAO.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=tasks.TaskResponse)
async def update_task(task_id: int, task_data: tasks.TaskUpdate, db: AsyncSession = Depends(get_db)):
    """Обновляет данные задачи."""
    task = await TaskDAO.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task_data.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.datetime.utcnow()  # Обновляем поле updated_at
    query = (
        tasks.Task.__table__.update()
        .where(tasks.Task.id == task_id)
        .values(**update_data)
        .returning(tasks.Task.__table__)
    )
    result = await db.execute(query)
    await db.commit()
    updated_task = result.first()
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found after update")
    return updated_task

@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет задачу по ID."""
    task = await TaskDAO.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    query = tasks.Task.__table__.delete().where(tasks.Task.id == task_id)
    await db.execute(query)
    await db.commit()
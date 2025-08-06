from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from app.database import get_db
from app.dao.models_dao import ProjectDAO
import logging

logger = logging.getLogger(__name__)

async def cmd_projects(message: Message):
    async for db in get_db():
        try:
            projects = await ProjectDAO.get_all(db)
            if not projects:
                await message.answer("Пока нет доступных проектов.")
                return

            response = "Список проектов:\n\n"
            for project in projects:
                response += f"📌 {project.title}\n"
                response += f"Описание: {project.description or 'Без описания'}\n"
                if project.project_url:
                    response += f"Ссылка: {project.project_url}\n"
                response += f"Дата завершения: {project.date_completed or 'Не указана'}\n\n"
            await message.answer(response)
        except Exception as e:
            logger.error(f"Error fetching projects: {str(e)}")
            await message.answer("Произошла ошибка при получении проектов.")
        break

def register_projects_handlers(dp: Dispatcher):
    dp.message.register(cmd_projects, Command("projects"))
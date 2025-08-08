from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters import Command
from app.database import get_db
from app.dao.models_dao import ProjectDAO
import logging

logger = logging.getLogger(__name__)

async def cmd_projects(message: Message):
    logger.debug("Processing /projects command")
    try:
        async for db in get_db():
            projects = await ProjectDAO.get_all(db)
            if not projects:
                await message.answer("Пока нет проектов, но скоро зажжём! 🔥", parse_mode="MarkdownV2")
                return
            response = "Мои проекты:\n\n"
            for project in projects:
                response += (
                    f"*{project.title}*\n"
                    f"{project.description or 'Крутой проект, но описания пока нет!'}\n"
                    f"[Залетай]({project.project_url or 'https://github.com/SUKUNA-AI'}) 🚀\n\n"
                )
            await message.answer(response, parse_mode="MarkdownV2")
            logger.info(f"Sent projects list to user {message.from_user.id}")
            break  # Используем одну сессию
    except Exception as e:
        logger.error(f"Error processing /projects: {str(e)}")
        await message.answer("Баги? Это фичи! 😎 Но что-то пошло не так, залетай позже! 🚀", parse_mode="MarkdownV2")

def register_projects_handlers(dp: Dispatcher, bot: Bot):
    dp.message.register(cmd_projects, Command(commands=["projects"]))
from aiogram import Bot
from app.database import get_db
from app.dao.models_dao import TelegramSubscriberDAO
import logging

logger = logging.getLogger(__name__)

async def notify_subscribers_new_project(bot: Bot, project):
    async for db in get_db():
        try:
            subscribers = await TelegramSubscriberDAO.get_all(db)
            for subscriber in subscribers:
                try:
                    await bot.send_message(
                        chat_id=subscriber.telegram_user_id,
                        text=(
                            f"🆕 Новый проект: {project.title}\n"
                            f"Описание: {project.description or 'Без описания'}\n"
                            f"Ссылка: {project.project_url or 'Не указана'}\n"
                            f"Дата завершения: {project.date_completed or 'Не указана'}"
                        )
                    )
                    logger.info(f"Sent project notification to {subscriber.telegram_user_id}")
                except Exception as e:
                    logger.error(f"Failed to send notification to {subscriber.telegram_user_id}: {str(e)}")
        except Exception as e:
            logger.error(f"Error fetching subscribers: {str(e)}")
        break
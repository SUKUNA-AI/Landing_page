from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from app.database import get_db
from app.dao.models_dao import TelegramSubscriberDAO
import logging

logger = logging.getLogger(__name__)

async def cmd_start(message: Message):
    telegram_user_id = str(message.from_user.id)
    username = message.from_user.username or "unknown"
    logger.info(f"New user started bot: {telegram_user_id} ({username})")

    async for db in get_db():
        try:
            subscriber = await TelegramSubscriberDAO.get_by_telegram_user_id(db, telegram_user_id)
            if not subscriber:
                await TelegramSubscriberDAO.create(db, {"telegram_user_id": telegram_user_id})
                await message.answer("Добро пожаловать! Вы успешно зарегистрированы.")
            else:
                await message.answer("Вы уже зарегистрированы!")
        except Exception as e:
            logger.error(f"Error registering user {telegram_user_id}: {str(e)}")
            await message.answer("Произошла ошибка при регистрации. Попробуйте позже.")
        break

def register_start_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
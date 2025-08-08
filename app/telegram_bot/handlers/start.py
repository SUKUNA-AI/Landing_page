from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from app.database import get_db
from app.dao.models_dao import TelegramSubscriberDAO
import logging

logger = logging.getLogger(__name__)

commands_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/projects"), KeyboardButton(text="/help")],
        [KeyboardButton(text="/postupdate")],
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

async def cmd_start(message: Message):
    telegram_user_id = str(message.from_user.id)
    username = message.from_user.username or "unknown"
    logger.info(f"User {telegram_user_id} ({username}) started bot")

    async for db in get_db():
        try:
            subscriber = await TelegramSubscriberDAO.get_by_telegram_user_id(db, telegram_user_id)
            if not subscriber:
                await TelegramSubscriberDAO.create(db, {"telegram_user_id": telegram_user_id})
                await message.answer(
                    "Добро пожаловать! 🚀 Вы успешно зарегистрированы.\n"
                    "Используйте команды ниже или задайте вопрос о портфолио: 💻",
                    reply_markup=commands_keyboard
                )
            else:
                await message.answer(
                    "Вы уже зарегистрированы! Используйте команды или задайте вопрос: 🔥",
                    reply_markup=commands_keyboard
                )
        except Exception as e:
            logger.error(f"Error registering user {telegram_user_id}: {str(e)}")
            await message.answer("Произошла ошибка при регистрации. Попробуйте позже. 😕")
        break

def register_start_handlers(dp: Dispatcher, bot: Bot):
    dp.message.register(cmd_start, Command("start"))
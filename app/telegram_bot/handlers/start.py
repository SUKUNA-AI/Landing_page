from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from app.database import get_db
from app.dao.models_dao import TelegramSubscriberDAO
import logging
import re

logger = logging.getLogger(__name__)

def escape_markdown_v2(text: str) -> str:
    """Экранирует специальные символы для MarkdownV2."""
    reserved_chars = r'([_\*[\]()~`>#\+-=|{}.!])'
    return re.sub(reserved_chars, r'\\\g<1>', text)

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

    try:
        async for db in get_db():
            try:
                subscriber = await TelegramSubscriberDAO.get_by_telegram_user_id(db, telegram_user_id)
                if not subscriber:
                    await TelegramSubscriberDAO.create(db, {"telegram_user_id": telegram_user_id})
                    await message.answer(
                        escape_markdown_v2("Добро пожаловать, братишка! 🚀 Ты в игре!\nИспользуй кнопки ниже или задай вопрос о портфолио: 💻"),
                        reply_markup=commands_keyboard, parse_mode="MarkdownV2"
                    )
                else:
                    await message.answer(
                        escape_markdown_v2("С возвращением, кодер! 🔥 Используй команды или задай вопрос: 💻"),
                        reply_markup=commands_keyboard, parse_mode="MarkdownV2"
                    )
                logger.info(f"User {telegram_user_id} processed successfully")
                break
            except Exception as e:
                logger.error(f"Error registering user {telegram_user_id}: {str(e)}")
                await message.answer(escape_markdown_v2("Ошибка при регистрации, попробуй позже! 😕"), parse_mode="MarkdownV2")
                break
    except Exception as e:
        logger.error(f"Error accessing database for user {telegram_user_id}: {str(e)}")
        await message.answer(escape_markdown_v2("Баги? Это фичи! 😎 Но что-то пошло не так, залетай позже! 🚀"), parse_mode="MarkdownV2")

def register_start_handlers(dp: Dispatcher, bot: Bot):
    dp.message.register(cmd_start, Command("start"))
from aiogram import Dispatcher, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import logging

logger = logging.getLogger(__name__)

help_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/projects"), KeyboardButton(text="/help")],
        [KeyboardButton(text="/postupdate")],
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

async def cmd_help(message: Message):
    logger.info(f"User {message.from_user.id} requested help")
    help_text = (
        "📋 **Доступные команды**:\n\n"
        "/start - Зарегистрироваться и начать работу с ботом 🚀\n"
        "/projects - Показать список всех проектов 📂\n"
        "/help - Показать это сообщение ℹ️\n"
        "/postupdate - Опубликовать обновления из GitHub (только для админа) 🔍\n\n"
        "Вы также можете задать вопрос о портфолио в текстовом формате.\n"
        "Используйте кнопки ниже для быстрого доступа к командам: 💻"
    )
    await message.answer(help_text, reply_markup=help_keyboard, parse_mode="Markdown")

def register_help_handlers(dp: Dispatcher, bot: Bot):
    dp.message.register(cmd_help, Command("help"))
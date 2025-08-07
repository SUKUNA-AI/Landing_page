from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import logging

logger = logging.getLogger(__name__)

# Создаём клавиатуру с кнопками для команд
help_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/start")],
        [KeyboardButton(text="/projects")],
        [KeyboardButton(text="/help")],
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

async def cmd_help(message: Message):
    logger.info(f"User {message.from_user.id} requested help")
    help_text = (
        "📋 Доступные команды:\n\n"
        "/start - Зарегистрироваться и начать работу с ботом\n"
        "/projects - Показать список всех проектов\n"
        "/help - Показать это сообщение\n\n"
        "Используйте кнопки ниже для быстрого доступа к командам:"
    )
    await message.answer(help_text, reply_markup=help_keyboard)

def register_help_handlers(dp: Dispatcher):
    dp.message.register(cmd_help, Command("help"))
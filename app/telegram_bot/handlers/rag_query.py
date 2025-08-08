from aiogram import Dispatcher, Bot
from aiogram.types import Message
from app.database import get_db
from app.telegram_bot.handlers.rag import register_rag_handlers
import logging

logger = logging.getLogger(__name__)

async def handle_text_query(message: Message):
    async for db in get_db():
        try:
            response = await register_rag_query_handlers(message.text, db)
            await message.answer(response)
        except Exception as e:
            logger.error(f"Error processing text query: {str(e)}")
            await message.answer("Ошибка при обработке вопроса. Попробуйте позже. 😕")

def register_rag_query_handlers(dp: Dispatcher, bot: Bot):
    dp.message.register(handle_text_query, lambda message: message.text and not message.text.startswith('/'))
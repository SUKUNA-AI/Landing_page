from aiogram import Dispatcher, F
from aiogram.types import Message
from app.services.rag import get_rag_response
from app.database import get_db
import logging

logger = logging.getLogger(__name__)

async def process_text_query(message: Message):
    query = f"Ответь на запрос как IT-гуру 2025 года. Стиль: дерзкий, с юмором (например, 'Баги? Это фичи!'). Используй эмодзи (🔥🚀💻) и сленг ('залетай', 'качаем'). Максимум 500 символов. Запрос: '{message.text}'"
    logger.debug(f"Processing query: {query}")
    async for db in get_db():
        try:
            response = await get_rag_response(query, db)
            await message.answer(response, parse_mode="Markdown")
            logger.info(f"Replied to query: {message.text}")
        except Exception as e:
            logger.error(f"Error processing query '{message.text}': {str(e)}")
            await message.answer("Баги? Это фичи! 😎 Но что-то пошло не так, залетай позже! 🚀")
        break  # Используем одну сессию

def register_rag_query_handlers(dp: Dispatcher):
    dp.message.register(process_text_query, F.text & ~F.text.startswith(("/", "!")))
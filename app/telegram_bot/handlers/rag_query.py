from aiogram import Dispatcher, F
from aiogram.types import Message
from app.services.rag import get_rag_response
from app.database import get_db
import logging
import re

logger = logging.getLogger(__name__)

def escape_markdown_v2(text: str) -> str:
    """Экранирует специальные символы для MarkdownV2."""
    reserved_chars = r'([_\*[\]()~`>#\+-=|{}.!])'
    return re.sub(reserved_chars, r'\\\g<1>', text)

async def process_text_query(message: Message):
    query = f"Ответь на запрос как IT-гуру 2025 года. Стиль: дерзкий, с юмором (например, 'Баги? Это фичи!'). Используй эмодзи (🔥🚀💻) и сленг ('залетай', 'качаем'). Максимум 500 символов. Запрос: '{message.text}'"
    logger.debug(f"Processing query: {query}")
    async for db in get_db():
        try:
            response = await get_rag_response(query, db)
            await message.answer(escape_markdown_v2(response), parse_mode="MarkdownV2")
            logger.info(f"Replied to query: {message.text}")
        except Exception as e:
            logger.error(f"Error processing query '{message.text}': {str(e)}")
            await message.answer(escape_markdown_v2("Баги? Это фичи! 😎 Но что-то пошло не так, залетай позже! 🚀"), parse_mode="MarkdownV2")
        break  # Используем одну сессию

def register_rag_query_handlers(dp: Dispatcher):
    dp.message.register(process_text_query, F.text & ~F.text.startswith(("/", "!")))
from aiogram import Dispatcher, Bot, F
from aiogram.types import Message
from app.services.rag import get_rag_response
from app.database import get_db
import logging
import re

logger = logging.getLogger(__name__)

def escape_markdown_v2(text: str) -> str:
    """Экранирует специальные символы для MarkdownV2."""
    reserved_chars = r'([_\*[\]()~`>#\+-=|{}\.!])'
    text = re.sub(reserved_chars, r'\\\g<1>', text)
    text = re.sub(r'([\\]{2,})', r'\\', text)
    return text[:1500]  # Увеличили лимит до 1500 символов

async def process_text_query(message: Message):
    query = f"Ты ассистент для портфолио IT-специалиста. Отвечай профессионально, но доступно, без сленга. Максимум 1500 символов. Используй эмодзи (🔥🚀💻) для акцента. Вопрос: '{message.text.encode('utf-8', errors='replace').decode('utf-8')}'"
    logger.debug(f"Processing query: {query}")
    async for db in get_db():
        try:
            response = await get_rag_response(query, db)
            escaped_response = escape_markdown_v2(response)
            await message.answer(escaped_response, parse_mode="MarkdownV2")
            logger.info(f"Replied to query: {message.text}")
        except Exception as e:
            logger.error(f"Error processing query '{message.text}': {str(e)}")
            fallback = "К сожалению, произошла ошибка. Попробуйте позже! 🚀"
            await message.answer(escape_markdown_v2(fallback), parse_mode="MarkdownV2")
        break

def register_rag_query_handlers(dp: Dispatcher, bot: Bot):
    dp.message.register(process_text_query, F.text & ~F.text.startswith(("/", "!")))
# В файле app/telegram_bot/handlers/rag_query.py
# Обновляем для вызова локального API вместо прямого вызова get_rag_response

from aiogram import Dispatcher, Bot, F
from aiogram.types import Message
import aiohttp
import logging
import re

logger = logging.getLogger(__name__)

def escape_markdown_v2(text: str) -> str:
    """Экранирует специальные символы для MarkdownV2."""
    reserved_chars = r'([_\*[\]()~`>#\+-=|{}\.!])'
    text = re.sub(reserved_chars, r'\\\g<1>', text)
    text = re.sub(r'([\\]{2,})', r'\\', text)  # Удаляем дублирующиеся слеши
    return text[:3510]

async def process_text_query(message: Message):
    """
    Обработчик текстовых запросов к RAG-агенту через Telegram.
    Вызывает локальный FastAPI эндпоинт /api/rag/.
    """
    query = message.text
    logger.debug(f"Processing query: {query.encode('utf-8')}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8000/api/rag/",  # Локальный URL FastAPI
                json={"question": query}
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    response = data["answer"]
                    escaped_response = escape_markdown_v2(response)
                    await message.answer(escaped_response, parse_mode="MarkdownV2")
                    logger.info(f"Replied to query: {query}")
                else:
                    logger.error(f"Failed to fetch RAG response: {resp.status}")
                    fallback = "Баги? Это фичи! 😎 Но что-то пошло не так, залетай позже! 🚀"
                    await message.answer(escape_markdown_v2(fallback), parse_mode="MarkdownV2")
    except Exception as e:
        logger.error(f"Error processing query '{query}': {str(e)}")
        fallback = "Баги? Это фичи! 😎 Но что-то пошло не так, залетай позже! 🚀"
        await message.answer(escape_markdown_v2(fallback), parse_mode="MarkdownV2")

def register_rag_query_handlers(dp: Dispatcher, bot: Bot):
    dp.message.register(process_text_query, F.text & ~F.text.startswith(("/", "!")))
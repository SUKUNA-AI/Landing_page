from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters import Command
from app.services.github_service import get_latest_commits, find_latest_active_repo
from app.telegram_bot.handlers.rag import format_post_with_gemini
from app.config import settings
import logging
import re

logger = logging.getLogger(__name__)

def escape_markdown_v2(text: str) -> str:
    """Экранирует специальные символы для MarkdownV2."""
    reserved_chars = r'([_\*[\]()~`>#\+-=|{}.!])'
    return re.sub(reserved_chars, r'\\\g<1>', text)

async def cmd_postupdate(message: Message, bot: Bot):
    if message.from_user.id != settings.ADMIN_TELEGRAM_ID:
        await message.answer(escape_markdown_v2("Только админ может постить обновления! 😎"), parse_mode="MarkdownV2")
        logger.warning(f"Unauthorized post attempt by user {message.from_user.id}")
        return

    repo_name = await find_latest_active_repo()
    if not repo_name:
        await message.answer(escape_markdown_v2("Репозитории не найдены! 😕"), parse_mode="MarkdownV2")
        logger.warning("No repositories found for manual post.")
        return

    commits = await get_latest_commits(repo_name)
    if not commits:
        await message.answer(escape_markdown_v2(f"Коммиты в {repo_name} не найдены! 😕"), parse_mode="MarkdownV2")
        logger.warning(f"No commits found for {repo_name}.")
        return

    try:
        message_text = await format_post_with_gemini(repo_name, commits)
        await bot.send_message(
            chat_id=settings.CHANNEL_ID,
            text=message_text,
            parse_mode="MarkdownV2"
        )
        await message.answer(escape_markdown_v2("Пост отправлен в канал! 🔥"), parse_mode="MarkdownV2")
        logger.info(f"Manual post from {repo_name} to {settings.CHANNEL_ID} by user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Failed to post update: {str(e)}")
        await message.answer(escape_markdown_v2("Баги? Это фичи! 😎 Но пост не удался, попробуй позже! 🚀"), parse_mode="MarkdownV2")

def register_channel_handlers(dp: Dispatcher, bot: Bot):
    dp.message.register(cmd_postupdate, Command(commands=["postupdate"]))
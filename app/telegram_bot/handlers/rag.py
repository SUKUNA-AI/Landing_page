from aiogram import Bot, Dispatcher
from app.services.github_service import get_latest_commits, find_latest_active_repo
from app.config import settings
from langchain_google_genai import ChatGoogleGenerativeAI
import logging
import asyncio
import re

logger = logging.getLogger(__name__)

def escape_markdown_v2(text: str) -> str:
    """Экранирует специальные символы для MarkdownV2."""
    reserved_chars = r'([_\*[\]()~`>#\+-=|{}.!])'
    text = re.sub(reserved_chars, r'\\\g<1>', text)
    text = text.replace('\n', '\n\n')  # Двойной перенос для читаемости
    return text[:500]

async def format_post_with_gemini(repo_name: str, commits: list) -> str:
    """Форматирует пост для Telegram с помощью Gemini-2.5-flash."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=settings.GEMINI_API_KEY)
    prompt = (
        f"Создай дерзкий и весёлый пост для Telegram о свежих коммитах в репо {repo_name}. "
        f"Используй сленг из повседневной жизни и эмодзи (🔥🚀💻). Макс. 1500 символов. "
        f"Коммиты: {', '.join([c['message'] for c in commits])}. "
        f"URL репо: https://github.com/{settings.GITHUB_USER}/{repo_name}"
    )
    try:
        response = llm.invoke(prompt)
        if not response.content:
            logger.warning("Gemini response is empty")
            fallback = (
                f"🆕 Свежак в *{repo_name}*! 🔥 "
                f"Коммиты: {', '.join([c['message'][:30] + '...' for c in commits[:3]]) or 'Пока тихо'}. "
                f"[Залетай](https://github.com/{settings.GITHUB_USER}/{repo_name}) \\🚀"
            )
            return escape_markdown_v2(fallback)
        return escape_markdown_v2(response.content)
    except Exception as e:
        logger.error(f"Gemini error: {str(e)}")
        fallback = (
            f"🆕 Свежак в *{repo_name}*! 🔥 "
            f"Коммиты: {', '.join([c['message'][:30] + '...' for c in commits[:3]]) or 'Пока тихо'}. "
            f"[Залетай](https://github.com/{settings.GITHUB_USER}/{repo_name}) \\🚀"
        )
        return escape_markdown_v2(fallback)

async def check_and_post_updates(bot: Bot):
    repo_name = await find_latest_active_repo()
    if not repo_name:
        logger.warning("No repositories found.")
        return

    commits = await get_latest_commits(repo_name)
    if not commits:
        logger.warning(f"No commits found for {repo_name}.")
        return

    try:
        message = await format_post_with_gemini(repo_name, commits)
        await bot.send_message(
            chat_id=settings.CHANNEL_ID,
            text=message,
            parse_mode="MarkdownV2"
        )
        logger.info(f"Auto-posted from {repo_name} to {settings.CHANNEL_ID}")
    except Exception as e:
        logger.error(f"Failed to post update for {repo_name}: {str(e)}")

async def start_autoposting(bot: Bot):
    """Запускает задачу автопостинга при старте бота."""
    async def scheduled_update():
        while True:
            await check_and_post_updates(bot)
            await asyncio.sleep(3600)  # Раз в час

    logger.info("Starting autoposting task...")
    asyncio.create_task(scheduled_update())

async def register_rag_handlers(dp: Dispatcher, bot: Bot):
    try:
        chat = await bot.get_chat(settings.CHANNEL_ID)
        logger.info(f"Channel accessible: {chat.id}, {chat.title}")
    except Exception as e:
        logger.error(f"Cannot access channel {settings.CHANNEL_ID}: {str(e)}")

    async def on_startup():
        await start_autoposting(bot)

    dp.startup.register(on_startup)
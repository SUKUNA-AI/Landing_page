import logging
import asyncio
import aiohttp

from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from app.database import get_db
from app.dao.models_dao import ProjectDAO
from app.services.github_service import find_latest_active_repo, get_latest_commits
from app.config import settings

from sqlalchemy.future import select
from app.models import Project  # Добавь, если Project не импортирован

from google import genai

logger = logging.getLogger(__name__)
GITHUB_HEADERS = {"Authorization": f"token {settings.GITHUB_TOKEN}"}


async def get_repo_description(repo_name: str) -> dict:
    url = f"https://api.github.com/repos/{settings.GITHUB_USER}/{repo_name}"
    fallback = {
        "name": repo_name,
        "description": "Крутой проект, но описания пока нет! 😎",
        "url": f"https://github.com/{settings.GITHUB_USER}/{repo_name}"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=GITHUB_HEADERS) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch repo {repo_name}: {response.status}")
                    return fallback
                repo = await response.json()
                return {
                    "name": repo["name"],
                    "description": repo["description"] or fallback["description"],
                    "url": repo["html_url"]
                }
        except aiohttp.ClientError as e:
            logger.error(f"Network error fetching repo {repo_name}: {e}")
            return fallback


async def moderate_comment(message: Message):
    if str(message.chat.id) != settings.CHANNEL_ID or not message.text:
        return

    logger.info(f"Moderating comment: {message.text}")

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=(
                f"Проанализируй комментарий: '{message.text}'. "
                "Верни 'clean', если норм, 'spam' — если неуместен."
            )
        )

        result = getattr(response, "text", None)
        if not result:
            logger.error("Gemini: no text in response")
            return

        if result.strip() == "spam":
            await message.delete()
            logger.info(f"Deleted spam: {message.text}")
            if message.from_user:
                await message.bot.send_message(
                    message.from_user.id,
                    "Комментарий удалён: спам или оффтоп. Пиши по делу, котик! 😼"
                )

    except Exception as e:
        logger.error(f"Error moderating comment: {e}")


async def reply_to_comment(message: Message):
    if str(message.chat.id) != settings.CHANNEL_ID or not message.text:
        return

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=(
                f"Ответь на комментарий как IT-энтузиаст с юмором и эмодзи 🔥🚀💻: '{message.text}'"
            ),
            config=genai.types.GenerateContentConfig(
                temperature=0.9,
                max_output_tokens=500
            )
        )

        result = getattr(response, "text", None)
        if not result:
            await message.reply("Ой, что-то сломалось 😅 Пиши ещё!")
            return

        await message.reply(result)
        logger.info(f"Ответ на коммент: {message.text}")

    except Exception as e:
        logger.error(f"Error replying to comment: {e}")
        await message.reply("Ой, всё упало... но я встану! 🤖 Пиши ещё!")


async def format_post(latest_repo: str, commits: list, db) -> str:
    commit_block = "\n".join(
        f"- **{c['message']}** (by {c['author']})\n"
        f"  Файлы: {', '.join(c.get('files', [])) or 'Без изменений'}\n"
        f"  [Коммит]({c['url']})"
        for c in commits
    )

    result = await db.execute(
        select(Project).filter_by(project_url=f"https://github.com/{settings.GITHUB_USER}/{latest_repo}")
    )
    project = result.scalars().first()

    project_block = (
        f"📂 **{project.title}**\n"
        f"{project.description or 'Крутой проект, но описания пока нет! 😎'}\n"
        f"[Перейти]({project.project_url})"
    ) if project else (
        f"📂 **{latest_repo}**\nКрутой проект, но описания пока нет! 😎\n"
        f"[Перейти](https://github.com/{settings.GITHUB_USER}/{latest_repo})"
    )

    prompt = (
        f"Напиши пост в Telegram-канал про свежие коммиты. Стиль: дерзкий, с эмодзи и юмором 🤖🔥💻\n"
        f"Макс 300 символов, пиши на русском, Markdown формат.\n\n"
        f"Репозиторий: {latest_repo}\n"
        f"Коммиты:\n{commit_block}\n"
        f"Проект:\n{project_block}"
    )

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.9,
                max_output_tokens=300
            )
        )

        result = getattr(response, "text", None)
        if not result:
            raise ValueError("Empty Gemini response")

        return result[:4096]

    except Exception as e:
        logger.error(f"Error generating post: {e}")
        return (
            f"🔥 Апдейт в [{latest_repo}](https://github.com/{settings.GITHUB_USER}/{latest_repo})! 🚀\n\n"
            f"{commit_block}\n\n{project_block}\n\nКодим? Пиши в комменты! 💻🤖"
        )[:4096]


async def post_github_update(message: Message, bot: Bot):
    if str(message.from_user.id) != str(settings.ADMIN_TELEGRAM_ID):
        await message.answer("Эта команда только для админа 😎")
        return

    logger.info(f"Admin {message.from_user.id} запустил GitHub постинг")

    async for db in get_db():
        try:
            latest_repo = await find_latest_active_repo()
            if not latest_repo:
                await message.answer("Репозиториев не найдено 😕")
                return

            commits = await get_latest_commits(latest_repo)
            if not commits:
                await message.answer("Коммитов нет 😅")
                return

            post = await format_post(latest_repo, commits, db)

            try:
                await bot.send_message(settings.CHANNEL_ID, post, parse_mode="Markdown")
                await message.answer("Пост в канале! 🎉")
            except TelegramBadRequest as e:
                logger.error(f"Send error: {e}")
                await message.answer("Не удалось отправить пост. Проверь права бота и CHANNEL_ID 😕")

        except aiohttp.ClientError as e:
            logger.error(f"GitHub network error: {e}")
            await message.answer("Ошибка GitHub 😅")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            await message.answer("Ошибка при публикации 😢")


async def auto_post_updates(bot: Bot):
    while True:
        async for db in get_db():
            try:
                try:
                    chat = await bot.get_chat(settings.CHANNEL_ID)
                    logger.info(f"Канал доступен: {chat.id} | {chat.title}")
                except TelegramBadRequest as e:
                    logger.error(f"Канал не доступен: {e}")
                    await asyncio.sleep(86400)
                    continue

                latest_repo = await find_latest_active_repo()
                if not latest_repo:
                    logger.warning("Нет активных репозиториев")
                    await asyncio.sleep(86400)
                    continue

                commits = await get_latest_commits(latest_repo)
                if not commits:
                    logger.warning(f"Нет коммитов в {latest_repo}")
                    await asyncio.sleep(86400)
                    continue

                post = await format_post(latest_repo, commits, db)
                try:
                    await bot.send_message(settings.CHANNEL_ID, post, parse_mode="Markdown")
                    logger.info(f"Автопост: {latest_repo}")
                except TelegramBadRequest as e:
                    logger.error(f"Auto-post error: {e}")

            except Exception as e:
                logger.error(f"Fatal auto-post error: {e}")

        await asyncio.sleep(86400)


def register_rag_handlers(dp: Dispatcher, bot: Bot):
    dp.message.register(moderate_comment, F.chat.type == ChatType.CHANNEL)
    dp.message.register(reply_to_comment, F.chat.type == ChatType.CHANNEL)
    dp.message.register(post_github_update, Command(commands=["postupdate"]))

    async def start_auto_posting():
        asyncio.create_task(auto_post_updates(bot))

    dp.startup.register(start_auto_posting)

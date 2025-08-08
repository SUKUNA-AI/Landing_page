from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from app.database import get_db
from app.dao.models_dao import ProjectDAO
from app.services.github_service import find_latest_active_repo, get_latest_commits
from app.config import settings
from google import genai
import logging
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

async def get_repo_description(repo_name: str) -> dict:
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}
        url = f"https://api.github.com/repos/{settings.GITHUB_USER}/{repo_name}"
        try:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch repo {repo_name}: {response.status}")
                    return {"name": repo_name, "description": "Крутой проект, но описания пока нет! 😎", "url": f"https://github.com/{settings.GITHUB_USER}/{repo_name}"}
                repo = await response.json()
                return {
                    "name": repo["name"],
                    "description": repo["description"] or "Крутой проект, но описания пока нет! 😎",
                    "url": repo["html_url"]
                }
        except aiohttp.ClientError as e:
            logger.error(f"Network error fetching repo {repo_name}: {str(e)}")
            return {"name": repo_name, "description": "Крутой проект, но описания пока нет! 😎", "url": f"https://github.com/{settings.GITHUB_USER}/{repo_name}"}

async def moderate_comment(message: Message):
    if str(message.chat.id) != settings.CHANNEL_ID:
        return
    if not message.text:
        return
    logger.info(f"Moderating comment in channel: {message.text}")
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Проанализируй следующий комментарий на наличие спама или неуместного контента: '{message.text}'.\n"
                     "Верни 'clean', если комментарий нормальный, или 'spam', если он спам или неуместный."
        )
        if not hasattr(response, 'text') or response.text is None:
            logger.error("Gemini response has no text attribute")
            return
        result = response.text.strip()
        if result == "spam":
            await message.delete()
            logger.info(f"Deleted spam comment: {message.text}")
            if message.from_user:
                await message.bot.send_message(
                    message.from_user.id,
                    "Ваш комментарий удалён, так как он содержит спам. 😕 Пиши по теме! 🚀"
                )
    except Exception as e:
        logger.error(f"Gemini error moderating comment: {str(e)}")

async def reply_to_comment(message: Message):
    if str(message.chat.id) != settings.CHANNEL_ID or not message.text:
        return
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=(
                f"Ответь на комментарий в дружелюбном тоне, как IT-энтузиаст. "
                f"Используй эмодзи (🔥🚀💻) и юмор. Комментарий: '{message.text}'"
            ),
            config=genai.types.GenerateContentConfig(
                temperature=0.9,
                max_output_tokens=500
            )
        )
        if not hasattr(response, 'text') or response.text is None:
            logger.error("Gemini response has no text attribute")
            await message.reply("Ой, что-то сломалось! 😅 Пиши ещё, я отвечу! 🚀")
            return
        await message.reply(response.text)
        logger.info(f"Replied to comment: {message.text}")
    except Exception as e:
        logger.error(f"Gemini error replying to comment: {str(e)}")
        await message.reply("Ой, что-то сломалось! 😅 Пиши ещё, я отвечу! 🚀")

async def generate_post_content(latest_repo: str, commits: list, latest_project: dict) -> str:
    commit_details = "\n".join(
        f"- **{commit['message']}** (by {commit['author']})\n"
        f"  Файлы: {', '.join(commit.get('files', [])) or 'Без изменений'}\n"
        f"  [Коммит]({commit['url']})"
        for commit in commits
    )
    project_info = (
        f"📂 **{latest_project['name']}**\n"
        f"{latest_project['description']}\n"
        f"[Перейти]({latest_project['url']})"
    )
    prompt = (
        f"Напиши короткий пост для Telegram-канала о свежих обновлениях в GitHub. "
        f"Стиль: дерзкий, лаконичный, с IT-юмором (например, 'Баги? Не, не слышал!'). "
        f"Используй эмодзи (🔥🚀💻🤖). Максимум 300 символов. "
        f"Фокус на ключевых изменениях, без лишних деталей. "
        f"Призыв к действию: 'Кодим? Пиши в комменты!'. "
        f"Пиши на русском, в Markdown.\n\n"
        f"Репозиторий: {latest_repo}\n"
        f"Коммиты:\n{commit_details}\n"
        f"Проект:\n{project_info}"
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
        if not hasattr(response, 'text') or response.text is None:
            logger.error("Gemini response has no text attribute")
            return (
                f"🔥 Апдейт в [{latest_repo}](https://github.com/{settings.GITHUB_USER}/{latest_repo})! 🚀\n\n"
                f"{commit_details}\n\n{project_info}\n\nКодим? Пиши в комменты! 💻🤖"
            )[:4096]
        return response.text[:4096]
    except Exception as e:
        logger.error(f"Gemini error generating post: {str(e)}")
        return (
            f"🔥 Апдейт в [{latest_repo}](https://github.com/{settings.GITHUB_USER}/{latest_repo})! 🚀\n\n"
            f"{commit_details}\n\n{project_info}\n\nКодим? Пиши в комменты! 💻🤖"
        )[:4096]

async def post_github_update(message: Message, bot: Bot):
    if str(message.from_user.id) != str(settings.ADMIN_TELEGRAM_ID):
        await message.answer("Эта команда только для админа! 😎")
        return
    logger.info(f"Admin {message.from_user.id} requested GitHub update post")
    async for db in get_db():
        try:
            latest_repo = await find_latest_active_repo()
            if not latest_repo:
                await message.answer("Активных репозиториев не найдено. 😕")
                return
            commits = await get_latest_commits(latest_repo)
            if not commits:
                await message.answer("Коммиты не найдены. 😅")
                return
            latest_project = await get_repo_description(latest_repo)

            post = await generate_post_content(latest_repo, commits, latest_project)
            try:
                await bot.send_message(settings.CHANNEL_ID, post, parse_mode="Markdown")
                await message.answer("Пост в канале! 🎉")
            except TelegramBadRequest as e:
                logger.error(f"Failed to send to channel {settings.CHANNEL_ID}: {str(e)}")
                await message.answer(f"Ошибка: Не удалось отправить пост. Проверь CHANNEL_ID и права бота. 😕")
        except aiohttp.ClientError as e:
            logger.error(f"Network error fetching GitHub data: {str(e)}")
            await message.answer("Ошибка с GitHub. 😅")
        except Exception as e:
            logger.error(f"Unexpected error posting update: {str(e)}")
            await message.answer("Ошибка при публикации. 😢")

async def auto_post_updates(bot: Bot):
    while True:
        async for db in get_db():
            try:
                try:
                    chat = await bot.get_chat(settings.CHANNEL_ID)
                    logger.info(f"Channel accessible: {chat.id}, {chat.title}")
                except TelegramBadRequest as e:
                    logger.error(f"Cannot access channel {settings.CHANNEL_ID}: {str(e)}")
                    await asyncio.sleep(86400)
                    continue
                latest_repo = await find_latest_active_repo()
                if not latest_repo:
                    logger.warning("No active repositories found.")
                    await asyncio.sleep(86400)
                    continue
                commits = await get_latest_commits(latest_repo)
                if not commits:
                    logger.warning(f"No commits found for {latest_repo}.")
                    await asyncio.sleep(86400)
                    continue
                latest_project = await get_repo_description(latest_repo)

                post = await generate_post_content(latest_repo, commits, latest_project)
                try:
                    await bot.send_message(settings.CHANNEL_ID, post, parse_mode="Markdown")
                    logger.info(f"Auto-posted from {latest_repo} to {settings.CHANNEL_ID}")
                except TelegramBadRequest as e:
                    logger.error(f"Failed to auto-post to {settings.CHANNEL_ID}: {str(e)}")
            except aiohttp.ClientError as e:
                logger.error(f"Network error in auto-post: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error in auto-post: {str(e)}")
        await asyncio.sleep(86400)  # Раз в день

def register_channel_handlers(dp: Dispatcher, bot: Bot):
    dp.message.register(moderate_comment, F.chat.type == ChatType.CHANNEL)
    dp.message.register(reply_to_comment, F.chat.type == ChatType.CHANNEL)
    dp.message.register(post_github_update, Command(commands=["postupdate"]))
    async def start_auto_posting():
        asyncio.create_task(auto_post_updates(bot))
    dp.startup.register(start_auto_posting)
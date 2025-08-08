from typing import List, Dict, Optional
import aiohttp
from aiohttp import ClientError
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging
from app.config import settings
from app.models import Project, User

logger = logging.getLogger(__name__)

FIXED_USER_ID = 1  # Используем user_id=1, так как он есть в базе

async def get_repo_description(repo_name: str) -> Dict[str, str]:
    """Получает описание репозитория с GitHub."""
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}
        url = f"https://api.github.com/repos/{settings.GITHUB_USER}/{repo_name}"
        try:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch repo {repo_name}: {response.status}")
                    return {
                        "name": repo_name,
                        "description": "Крутой проект, но описания пока нет!",
                        "url": f"https://github.com/{settings.GITHUB_USER}/{repo_name}"
                    }
                repo = await response.json()
                return {
                    "name": repo["name"],
                    "description": repo["description"] or "Крутой проект, но описания пока нет!",
                    "url": repo["html_url"]
                }
        except ClientError as e:
            logger.error(f"Network error fetching repo {repo_name}: {str(e)}")
            return {
                "name": repo_name,
                "description": "Крутой проект, но описания пока нет!",
                "url": f"https://github.com/{settings.GITHUB_USER}/{repo_name}"
            }

async def fetch_repos() -> List[Dict]:
    """Получает список всех репозиториев пользователя с GitHub."""
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}
        url = f"https://api.github.com/users/{settings.GITHUB_USER}/repos"
        try:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch repos: {response.status}")
                    return []
                repos = await response.json()
                return [
                    {
                        "name": repo["name"],
                        "description": repo["description"],
                        "html_url": repo["html_url"],
                        "pushed_at": repo["pushed_at"]
                    }
                    for repo in repos
                ]
        except ClientError as e:
            logger.error(f"Network error fetching repos: {str(e)}")
            return []

async def get_default_branch(repo_name: str) -> Optional[str]:
    """Получает основную ветку репозитория."""
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}
        url = f"https://api.github.com/repos/{settings.GITHUB_USER}/{repo_name}"
        try:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch repo {repo_name}: {response.status}")
                    return "main"
                repo = await response.json()
                return repo.get("default_branch", "main")
        except ClientError as e:
            logger.error(f"Network error fetching default branch for {repo_name}: {str(e)}")
            return "main"

async def get_latest_commits(repo_name: str, branch: Optional[str] = None) -> List[Dict]:
    """Получает последние 5 коммитов из указанного репозитория и ветки."""
    if not branch:
        branch = await get_default_branch(repo_name)
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}
        url = f"https://api.github.com/repos/{settings.GITHUB_USER}/{repo_name}/commits?sha={branch}"
        try:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch commits for {repo_name}: {response.status}")
                    return []
                commits = await response.json()
                commit_details = []
                for commit in commits[:5]:
                    commit_url = commit["url"]
                    async with session.get(commit_url, headers=headers) as commit_response:
                        if commit_response.status == 200:
                            commit_data = await commit_response.json()
                            files = [file["filename"] for file in commit_data.get("files", [])]
                        else:
                            files = []
                            logger.warning(f"Failed to fetch commit details {commit_url}: {commit_response.status}")
                    commit_details.append({
                        "message": commit["commit"]["message"],
                        "author": commit["commit"]["author"]["name"],
                        "url": commit["html_url"],
                        "files": files
                    })
                return commit_details
        except ClientError as e:
            logger.error(f"Network error fetching commits for {repo_name}: {str(e)}")
            return []

async def find_latest_active_repo() -> Optional[str]:
    """Находит репозиторий с последней активностью."""
    repos = await fetch_repos()
    if not repos:
        logger.warning("No repositories found.")
        return None
    latest_repo = max(repos, key=lambda x: x["pushed_at"], default=None)
    return latest_repo["name"] if latest_repo else None

async def ensure_user_exists(session: AsyncSession, user_id: int, username: str) -> None:
    """Проверяет наличие пользователя в БД и создаёт его, если не существует."""
    result = await session.execute(select(User).filter_by(id=user_id))
    user = result.scalars().first()
    if not user:
        new_user = User(id=user_id, username=username)
        session.add(new_user)
        await session.flush()
        logger.info(f"Created user with id {user_id} and username {username}")

async def upsert_project(session: AsyncSession, data: Dict) -> None:
    """Обновляет или создаёт проект в БД."""
    result = await session.execute(select(Project).filter_by(project_url=data["project_url"]))
    project = result.scalars().first()
    if project:
        for key, value in data.items():
            setattr(project, key, value)
    else:
        session.add(Project(**data))
    await session.flush()

async def sync_projects_with_github(session: AsyncSession) -> None:
    """Синхронизирует проекты из GitHub с базой данных."""
    repos = await fetch_repos()
    if not repos:
        logger.warning("No repositories found to sync.")
        return

    await ensure_user_exists(session, FIXED_USER_ID, settings.GITHUB_USER)

    for repo in repos:
        project_data = {
            "user_id": FIXED_USER_ID,
            "title": repo["name"],
            "description": repo["description"] or "Крутой проект, но описания пока нет!",
            "image_url": None,
            "project_url": repo["html_url"],
            "date_completed": datetime.strptime(repo["pushed_at"], "%Y-%m-%dT%H:%M:%SZ")
        }
        try:
            await upsert_project(session, project_data)
            logger.info(f"Synced project: {repo['name']}")
        except Exception as e:
            logger.error(f"Failed to sync project {repo['name']}: {str(e)}")
            raise

    logger.info("All projects synced successfully.")
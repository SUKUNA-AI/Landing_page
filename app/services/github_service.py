import aiohttp
import logging
from datetime import datetime

from app.config import settings
from app.database import get_db
from app.dao.models_dao import ProjectDAO

logger = logging.getLogger(__name__)

GITHUB_API_BASE = "https://api.github.com"
HEADERS = {"Authorization": f"token {settings.GITHUB_TOKEN}"}


async def find_latest_active_repo():
    url = f"{GITHUB_API_BASE}/users/{settings.GITHUB_USER}/repos?sort=updated&per_page=1"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=HEADERS) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch repos: {response.status}")
                    return None

                repos = await response.json()
                return repos[0]["name"] if repos else None

        except aiohttp.ClientError as e:
            logger.error(f"Network error fetching repos: {e}")
            return None


async def get_latest_commits(repo_name: str, limit: int = 3):
    commits_url = f"{GITHUB_API_BASE}/repos/{settings.GITHUB_USER}/{repo_name}/commits?per_page={limit}"
    detailed_commits = []

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(commits_url, headers=HEADERS) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch commits for {repo_name}: {response.status}")
                    return []

                commits = await response.json()

                for commit in commits:
                    commit_sha = commit["sha"]
                    commit_url = f"{GITHUB_API_BASE}/repos/{settings.GITHUB_USER}/{repo_name}/commits/{commit_sha}"

                    async with session.get(commit_url, headers=HEADERS) as commit_response:
                        if commit_response.status != 200:
                            logger.error(f"Failed to fetch commit {commit_sha}: {commit_response.status}")
                            continue

                        commit_details = await commit_response.json()
                        files = commit_details.get("files", [])

                        file_changes = [
                            f"{f['filename']} (+{f.get('additions', 0)}/-{f.get('deletions', 0)})"
                            for f in files[:5]
                        ]

                        detailed_commits.append({
                            "message": commit["commit"]["message"],
                            "author": commit["commit"]["author"]["name"],
                            "sha": commit_sha,
                            "url": commit["html_url"].replace("Landingpage", "Landing_page"),
                            "files": file_changes,
                            "diff": files[0].get("patch", "No diff available") if files else "No files changed",
                        })

            return detailed_commits

        except aiohttp.ClientError as e:
            logger.error(f"Network error fetching commits: {e}")
            return []


async def sync_projects_with_github():
    url = f"{GITHUB_API_BASE}/users/{settings.GITHUB_USER}/repos"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=HEADERS) as response:
                if response.status != 200:
                    logger.error(f"Failed to fetch repos: {response.status}")
                    return

                repos = await response.json()

                async for db in get_db():
                    for repo in repos:
                        project_data = {
                            "user_id": settings.GITHUB_USER,
                            "title": repo["name"],
                            "description": repo["description"] or "No description",
                            "image_url": None,
                            "project_url": repo["html_url"],
                            "date_completed": datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ"),
                        }

                        try:
                            await ProjectDAO.create_or_update(db, project_data)
                            logger.info(f"Synced project: {repo['name']}")
                        except Exception as e:
                            logger.error(f"Error syncing project {repo['name']}: {e}")

        except aiohttp.ClientError as e:
            logger.error(f"Network error syncing repos: {e}")

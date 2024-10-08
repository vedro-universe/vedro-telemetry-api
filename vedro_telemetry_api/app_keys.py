from aiohttp.web import AppKey

from .repositories import SessionRepository

__all__ = ("session_repo_key",)

session_repo_key: AppKey[SessionRepository] = AppKey("session_repo")

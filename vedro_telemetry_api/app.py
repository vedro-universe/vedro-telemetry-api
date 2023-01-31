from aiohttp import web
from aiohttp.web import Application

from .clients import PgsqlClient
from .config import Config
from .handlers import healthcheck, post_events
from .repositories import SessionRepository

__all__ = ("create_app",)


async def create_app() -> Application:
    app = Application()

    pgsql_client = PgsqlClient(Config.Database.DSN)
    app["session_repo"] = SessionRepository(pgsql_client)

    app.add_routes([
        web.get("/healthcheck", healthcheck),
        web.post("/v1/events", post_events),
    ])

    return app

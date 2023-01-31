from aiohttp import web
from aiohttp.web import Application

from .clients import PgsqlClient
from .config import Config
from .handlers import healthcheck

__all__ = ("create_app",)


async def create_app() -> Application:
    app = Application()

    pgsql_client = PgsqlClient(Config.Database.DSN)
    app["pgsql_client"] = pgsql_client

    app.add_routes([
        web.get("/healthcheck", healthcheck),
    ])

    return app

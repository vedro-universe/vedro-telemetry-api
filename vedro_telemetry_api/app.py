from aiohttp import web
from aiohttp.web import Application

from .app_keys import session_repo_key
from .clients import PgsqlClient
from .config import Config
from .handlers.healthcheck import healthcheck
from .handlers.post_events import post_events
from .repositories import SessionRepository

__all__ = ("create_app",)


async def create_app() -> Application:
    """
    Create and configure the aiohttp web application.

    This function initializes the web application by setting up routes
    for health check and event posting, and it configures the session
    repository with a PostgreSQL client.

    Routes:
        - GET `/healthcheck`: For checking service health.
        - POST `/v1/events`: For posting telemetry events.

    :return: The fully configured `Application` instance.
    """
    app = Application()

    pgsql_client = PgsqlClient(Config.Database.DSN)
    app[session_repo_key] = SessionRepository(pgsql_client)

    app.add_routes([
        web.get("/healthcheck", healthcheck),
        web.post("/v1/events", post_events),
    ])

    return app

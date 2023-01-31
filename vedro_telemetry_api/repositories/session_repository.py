from ..clients import PgsqlClient
from .repository import Repository

__all__ = ("SessionRepository",)


class SessionRepository(Repository):
    def __init__(self, pgsql_client: PgsqlClient) -> None:
        self._pgsql_client = pgsql_client

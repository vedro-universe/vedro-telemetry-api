from contextlib import asynccontextmanager
from typing import AsyncGenerator

from asyncpg import Connection, connect

__all__ = ("PgsqlClient",)


class PgsqlClient:
    """
    Manages PostgreSQL database connections and transactions.

    This class provides asynchronous context managers for establishing
    a connection to a PostgreSQL database and for managing transactions.
    It ensures that connections are properly closed after usage.
    """

    def __init__(self, dsn: str) -> None:
        """
        Initialize the PgsqlClient with the given Data Source Name (DSN).

        :param dsn: The Data Source Name (DSN) used to connect to the PostgreSQL database.
        """
        self._dsn = dsn

    @asynccontextmanager
    async def connection(self) -> AsyncGenerator[Connection, None]:
        """
        Create an asynchronous context manager for a database connection.

        This method establishes a connection to the PostgreSQL database using the provided
        DSN and yields the connection. The connection is automatically closed when the context
        exits.

        :yield: An active PostgreSQL connection.
        """
        conn = await connect(self._dsn)
        try:
            yield conn
        finally:
            await conn.close()

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[Connection, None]:
        """
        Create an asynchronous context manager for a database transaction.

        This method manages a database transaction within a connection context.
        It ensures that a connection is opened, a transaction is started, and
        the transaction is either committed or rolled back depending on whether
        an exception occurs within the context.

        :yield: An active PostgreSQL connection wrapped in a transaction.
        """
        async with self.connection() as connection:
            async with connection.transaction():
                yield connection

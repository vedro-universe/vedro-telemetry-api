import json
from typing import Any, List, Tuple, TypeVar
from uuid import UUID

from ..clients import PgsqlClient
from ..entities import (
    ArgumentEntity,
    ExceptionEntity,
    PluginEntity,
    SessionEntity,
    SessionInfoEntity,
)
from ..utils import cut_str
from .repository import Repository

__all__ = ("SessionRepository",)

_T = TypeVar("_T")
QueryType = Tuple[str, List[_T]]


class SessionRepository(Repository):
    def __init__(self, pgsql_client: PgsqlClient) -> None:
        self._pgsql_client = pgsql_client

    def _make_session_query(self, session: SessionEntity) -> QueryType[Any]:
        query = """
            INSERT INTO sessions (
                id,
                project_id,

                inited_at,
                created_at,
                started_at,
                ended_at,
                saved_at,

                discovered,
                scheduled,
                total,
                passed,
                failed,
                skipped,

                cmd,
                interrupted
            )
            VALUES ($1, $2, $3, $4, NOW(), $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
        """
        cmd = json.dumps(session.cmd) if session.cmd else None
        interrupted = json.dumps(session.interrupted) if session.interrupted else None
        return query, [
            session.id,
            cut_str(session.project_id, 255),

            session.inited_at,
            session.created_at,
            session.started_at,
            session.ended_at,

            session.discovered,
            session.scheduled,
            session.total,
            session.passed,
            session.failed,
            session.skipped,

            cmd,
            interrupted,
        ]

    def _make_arguments_query(self, session_id: UUID,
                              arguments: List[ArgumentEntity]) -> QueryType[List[Any]]:
        query = """
            INSERT INTO arguments (session_id, name, value)
            VALUES ($1, $2, $3)
        """
        args = []
        for argument in arguments:
            args.append([
                session_id,
                cut_str(argument.name, 255),
                json.dumps(argument.value)
            ])

        return query, args

    def _make_plugins_query(self, session_id: UUID,
                            plugins: List[PluginEntity]) -> QueryType[List[Any]]:
        query = """
            INSERT INTO plugins (session_id, name, module, enabled, version)
             VALUES ($1, $2, $3, $4, $5)
        """
        args = []
        for plugin in plugins:
            args.append([
                session_id,
                cut_str(plugin.name, 255),
                cut_str(plugin.module, 1024),
                plugin.enabled,
                cut_str(plugin.version, 32),
            ])
        return query, args

    def _make_exceptions_query(self, session_id: UUID,
                               exceptions: List[ExceptionEntity]) -> QueryType[List[Any]]:
        query = """
            INSERT INTO exceptions (
                session_id,
                scenario_id,

                type,
                message,
                traceback,

                raised_at
            )
            VALUES ($1, $2, $3, $4, $5, $6)
        """
        args = []
        for exception in exceptions:
            args.append([
                session_id,
                cut_str(exception.scenario_id, 1024),

                cut_str(exception.type, 255),
                exception.message,
                exception.traceback,

                exception.raised_at,
            ])
        return query, args

    async def save_session(self, session_info: SessionInfoEntity) -> None:
        async with self._pgsql_client.transaction() as conn:
            session_id = session_info.session.id

            session_query, session_args = self._make_session_query(session_info.session)
            await conn.execute(session_query, *session_args)

            args_query, args_args = \
                self._make_arguments_query(session_id, session_info.arguments)
            await conn.executemany(args_query, args_args)

            plugins_query, plugins_args = \
                self._make_plugins_query(session_id, session_info.plugins)
            await conn.executemany(plugins_query, plugins_args)

            exceptions_query, exceptions_args = \
                self._make_exceptions_query(session_id, session_info.exceptions)
            await conn.executemany(exceptions_query, exceptions_args)

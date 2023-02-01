import json
from typing import Any, List, Tuple
from uuid import UUID

from ..clients import PgsqlClient
from ..entities import (
    ArgumentEntity,
    ExceptionEntity,
    PluginEntity,
    SessionEntity,
    SessionInfoEntity,
)
from .repository import Repository

__all__ = ("SessionRepository",)


class SessionRepository(Repository):
    def __init__(self, pgsql_client: PgsqlClient) -> None:
        self._pgsql_client = pgsql_client

    def _make_session_query(self, session: SessionEntity) -> Tuple[str, List[Any]]:
        query = """
            INSERT INTO sessions (
                id,
                project_id,

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
            VALUES ($1, $2, $3, $4, NOW(), $5, $6, $7, $8, $9, $10, $11, $12)
        """
        cmd = json.dumps(session.cmd) if session.cmd else None
        interrupted = json.dumps(session.interrupted) if session.interrupted else None
        return query, [
            session.id,
            session.project_id,

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
                              arguments: List[ArgumentEntity]) -> Tuple[str, List[List[Any]]]:
        query = """
            INSERT INTO arguments (session_id, name, value)
            VALUES ($1, $2, $3)
        """
        args = []
        for argument in arguments:
            args.append([session_id, argument.name, json.dumps(argument.value)])

        return query, args

    def _make_plugins_query(self, session_id: UUID,
                            plugins: List[PluginEntity]) -> Tuple[str, List[List[Any]]]:
        query = """
            INSERT INTO plugins (session_id, name, module, enabled)
             VALUES ($1, $2, $3, $4)
        """
        args = []
        for plugin in plugins:
            args.append([session_id, plugin.name, plugin.module, plugin.enabled])
        return query, args

    def _make_exceptions_query(self, session_id: UUID,
                               exceptions: List[ExceptionEntity]) -> Tuple[str, List[List[Any]]]:
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
                exception.scenario_id,

                exception.type,
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

            args_query, args_args = self._make_arguments_query(session_id, session_info.arguments)
            await conn.executemany(args_query, args_args)

            plugins_query, plugins_args = self._make_plugins_query(session_id, session_info.plugins)
            await conn.executemany(plugins_query, plugins_args)

            exceptions_query, exceptions_args = self._make_exceptions_query(session_id, session_info.exceptions)
            await conn.executemany(exceptions_query, exceptions_args)

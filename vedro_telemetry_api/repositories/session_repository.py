import json
from typing import Any, List, Tuple

from ..clients import PgsqlClient
from ..entities import SessionEntity, SessionInfoEntity
from .repository import Repository

__all__ = ("SessionRepository",)


class SessionRepository(Repository):
    def __init__(self, pgsql_client: PgsqlClient) -> None:
        self._pgsql_client = pgsql_client

    def _make_create_session_query(self, session: SessionEntity) -> Tuple[str, List[Any]]:
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

    async def save_session(self, session_info: SessionInfoEntity) -> None:
        async with self._pgsql_client.transaction() as conn:
            session_query, session_args = self._make_create_session_query(session_info.session)
            await conn.execute(session_query, *session_args)

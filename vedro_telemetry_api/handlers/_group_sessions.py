from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID

from ..entities import (
    ArgumentEntity,
    ExceptionEntity,
    PluginEntity,
    SessionEntity,
    SessionInfoEntity,
)

__all__ = ("_group_sessions",)


def _ms_to_datetime(ms: int) -> datetime:
    return datetime.utcfromtimestamp(ms / 1000.0)


def _group_sessions(events: List[Dict[str, Any]]) -> Dict[UUID, SessionInfoEntity]:
    sessions = {}

    for event in events:
        event_id = event["event_id"]
        session_id = UUID(event["session_id"])
        created_at = _ms_to_datetime(event["created_at"])
        if session_id not in sessions:
            session = SessionEntity(session_id, created_at)
            sessions[session_id] = SessionInfoEntity(session)
        else:
            session = sessions[session_id].session

        if event_id == "StartedTelemetryEvent":
            session.project_id = event["project_id"]
            session.started_at = created_at
            for plugin in event["plugins"]:
                sessions[session_id].plugins.append(
                    PluginEntity(plugin["name"], plugin["module"], plugin["enabled"])
                )

        elif event_id == "ArgParseTelemetryEvent":
            session.cmd = event["cmd"]

        elif event_id == "ArgParsedTelemetryEvent":
            for name, value in event["args"].items():
                sessions[session_id].arguments.append(
                    ArgumentEntity(name, value)
                )

        elif event_id == "StartupTelemetryEvent":
            session.discovered = event["discovered"]
            session.scheduled = event["scheduled"]

        elif event_id == "ExcRaisedTelemetryEvent":
            exception = event["exception"]
            sessions[session_id].exceptions.append(
                ExceptionEntity(
                    type=exception["type"],
                    message=exception["message"],
                    traceback="".join(exception["traceback"]),
                    scenario_id=event["scenario_id"],
                    raised_at=created_at,
                )
            )

        elif event_id == "EndedTelemetryEvent":
            session.ended_at = created_at
            session.total = event["total"]
            session.passed = event["passed"]
            session.failed = event["failed"]
            session.skipped = event["skipped"]
            if event["interrupted"]:
                session.interrupted = {
                    "type": event["interrupted"]["type"],
                    "message": event["interrupted"]["message"],
                    "traceback": "".join(event["interrupted"]["traceback"]),
                }

        else:
            raise ValueError(f"Unknown event_id: {event_id}")

    return sessions

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
    """
    Convert milliseconds since epoch to a UTC datetime object.

    :param ms: The timestamp in milliseconds.
    :return: A `datetime` object representing the given timestamp.
    """
    return datetime.utcfromtimestamp(ms / 1000.0)


def _group_sessions(events: List[Dict[str, Any]]) -> Dict[UUID, SessionInfoEntity]:
    """
    Group events by session and construct `SessionInfoEntity` objects.

    This function processes a list of telemetry events, grouping them by session.
    It initializes or updates session-related data based on the event type, and
    returns a dictionary mapping session UUIDs to `SessionInfoEntity` instances.

    :param events: A list of event dictionaries containing telemetry data.
    :return: A dictionary where the keys are session UUIDs and the values are
             `SessionInfoEntity` instances populated with event data.
    :raises ValueError: If an unknown `event_id` is encountered.
    """
    sessions = {}

    for event in events:
        event_id = event["event_id"]
        session_id = UUID(event["session_id"])
        if session_id not in sessions:
            session = SessionEntity(session_id)
            sessions[session_id] = SessionInfoEntity(session)
        else:
            session = sessions[session_id].session

        if event_id == "StartedTelemetryEvent":
            session.project_id = event["project_id"]
            session.inited_at = _ms_to_datetime(event["inited_at"])
            session.created_at = _ms_to_datetime(event["created_at"])
            session.environment = event["environment"]
            for plugin in event["plugins"]:
                sessions[session_id].plugins.append(
                    PluginEntity(
                        name=plugin["name"],
                        module=plugin["module"],
                        enabled=plugin["enabled"],
                        version=plugin["version"],
                    )
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
            session.started_at = _ms_to_datetime(event["created_at"])

        elif event_id == "ExcRaisedTelemetryEvent":
            exception = event["exception"]
            sessions[session_id].exceptions.append(
                ExceptionEntity(
                    type=exception["type"],
                    message=exception["message"],
                    traceback="".join(exception["traceback"]),
                    scenario_id=event["scenario_id"],
                    raised_at=_ms_to_datetime(event["created_at"]),
                )
            )

        elif event_id == "EndedTelemetryEvent":
            session.ended_at = _ms_to_datetime(event["created_at"])
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

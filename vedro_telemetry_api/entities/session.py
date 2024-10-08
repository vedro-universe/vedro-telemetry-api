from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, TypedDict
from uuid import UUID

__all__ = ("SessionEntity",)


class InterruptedException(TypedDict):
    """
    Represents the structure of an interrupted exception.

    This TypedDict defines the expected keys and their corresponding value types
    for an interrupted exception, including the type of exception, the message,
    and the traceback.

    Keys:
        - type: The type of the exception as a string.
        - message: The exception message as a string.
        - traceback: The formatted traceback as a string.
    """
    type: str
    message: str
    traceback: str


class Environment(TypedDict):
    """
    Represents the structure of the environment information.

    This TypedDict defines the expected keys and their corresponding value types
    for environment details, including the Python version and the Vedro version
    in use.

    Keys:
        - python_version: The version of Python used, as a string.
        - vedro_version: The version of Vedro used, as a string.
    """
    python_version: str
    vedro_version: str


_utc_zero = datetime.utcfromtimestamp(0)


@dataclass
class SessionEntity:
    """
    Represents a test session and its associated data.

    This class holds information about a test session, including its ID, timestamps,
    project ID, discovered and scheduled test counts, results, and environment details.
    It also tracks if the session was interrupted by an exception.

    :param id: The unique identifier for the session.
    :param inited_at: The time when the session was initialized.
    :param created_at: The time when the session was created.
    :param started_at: The time when the session started.
    :param ended_at: The time when the session ended.
    :param project_id: The ID of the project related to the session.
    :param discovered: The number of tests discovered during the session.
    :param scheduled: The number of tests scheduled to run.
    :param total: The total number of tests run during the session.
    :param passed: The number of tests that passed.
    :param failed: The number of tests that failed.
    :param skipped: The number of tests that were skipped.
    :param cmd: The command-line arguments used for the session.
    :param environment: Information about the environment in which the session was run.
    :param interrupted: Details of any exception that interrupted the session.
    """
    id: UUID
    inited_at: datetime = _utc_zero
    created_at: datetime = _utc_zero

    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    project_id: str = ""

    discovered: Optional[int] = None
    scheduled: Optional[int] = None
    total: Optional[int] = None
    passed: Optional[int] = None
    failed: Optional[int] = None
    skipped: Optional[int] = None

    cmd: Optional[List[str]] = None
    environment: Optional[Environment] = None
    interrupted: Optional[InterruptedException] = None

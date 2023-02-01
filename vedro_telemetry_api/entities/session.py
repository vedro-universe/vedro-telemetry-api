from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, TypedDict
from uuid import UUID

__all__ = ("SessionEntity",)


class InterruptedException(TypedDict):
    type: str
    message: str
    traceback: str


@dataclass
class SessionEntity:
    id: UUID
    started_at: datetime
    ended_at: Optional[datetime] = None
    project_id: str = ""
    cmd: Optional[List[str]] = None

    discovered: Optional[int] = None
    scheduled: Optional[int] = None
    total: Optional[int] = None
    passed: Optional[int] = None
    failed: Optional[int] = None
    skipped: Optional[int] = None

    interrupted: Optional[InterruptedException] = None

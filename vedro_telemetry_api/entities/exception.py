from dataclasses import dataclass
from datetime import datetime

__all__ = ("ExceptionEntity",)


@dataclass
class ExceptionEntity:
    type: str
    message: str
    traceback: str
    scenario_id: str
    raised_at: datetime

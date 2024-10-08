from dataclasses import dataclass
from datetime import datetime

__all__ = ("ExceptionEntity",)


@dataclass
class ExceptionEntity:
    """
    Represents information about an exception raised during a session.

    This class captures details about an exception that occurred during the
    execution of a scenario, including the type, message, traceback, and the
    associated scenario ID.

    :param type: The type of the exception.
    :param message: The exception message.
    :param traceback: The formatted traceback string.
    :param scenario_id: The ID of the scenario where the exception was raised.
    :param raised_at: The timestamp when the exception occurred.
    """
    type: str
    message: str
    traceback: str
    scenario_id: str
    raised_at: datetime

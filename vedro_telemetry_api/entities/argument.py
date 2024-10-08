from dataclasses import dataclass
from typing import Any

__all__ = ("ArgumentEntity", )


@dataclass
class ArgumentEntity:
    """
    Represents a command-line argument used during a test session.

    This class stores the name and value of an argument passed to the
    test run, allowing it to be recorded for later analysis.

    :param name: The name of the argument.
    :param value: The value associated with the argument.
    """
    name: str
    value: Any

from dataclasses import dataclass, field
from typing import List

from .argument import ArgumentEntity
from .exception import ExceptionEntity
from .plugin import PluginEntity
from .session import SessionEntity

__all__ = ("SessionInfoEntity",)


@dataclass
class SessionInfoEntity:
    """
    Aggregates detailed information about a test session.

    This class combines the session entity with additional data, including
    command-line arguments, loaded plugins, and any exceptions raised during
    the session.

    :param session: The core session entity containing general session data.
    :param arguments: A list of arguments passed to the session.
    :param plugins: A list of plugins that were active during the session.
    :param exceptions: A list of exceptions that were raised during the session.
    """
    session: SessionEntity
    arguments: List[ArgumentEntity] = field(default_factory=list)
    plugins: List[PluginEntity] = field(default_factory=list)
    exceptions: List[ExceptionEntity] = field(default_factory=list)

from dataclasses import dataclass, field
from typing import List

from .argument import ArgumentEntity
from .exception import ExceptionEntity
from .plugin import PluginEntity
from .session import SessionEntity

__all__ = ("SessionInfoEntity",)


@dataclass
class SessionInfoEntity:
    session: SessionEntity
    arguments: List[ArgumentEntity] = field(default_factory=list)
    plugins: List[PluginEntity] = field(default_factory=list)
    exceptions: List[ExceptionEntity] = field(default_factory=list)

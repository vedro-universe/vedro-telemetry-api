from dataclasses import dataclass
from typing import Any

__all__ = ("ArgumentEntity", )


@dataclass
class ArgumentEntity:
    key: str
    value: Any

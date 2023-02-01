from dataclasses import dataclass
from typing import Any

__all__ = ("ArgumentEntity", )


@dataclass
class ArgumentEntity:
    name: str
    value: Any

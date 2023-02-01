from dataclasses import dataclass

__all__ = ("PluginEntity", )


@dataclass
class PluginEntity:
    name: str
    module: str
    enabled: bool
    version: str

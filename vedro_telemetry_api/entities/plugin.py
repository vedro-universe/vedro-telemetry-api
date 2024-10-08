from dataclasses import dataclass

__all__ = ("PluginEntity", )


@dataclass
class PluginEntity:
    """
    Represents a plugin's metadata and configuration.

    This class holds information about a plugin, including its name, module,
    whether it is enabled, and its version.
    """
    name: str
    module: str
    enabled: bool
    version: str

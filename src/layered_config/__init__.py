from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("layered-config-py")
except PackageNotFoundError:
    __version__ = "unknown"

from layered_config.layered_config import LayeredConfig

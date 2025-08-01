from .config_reader import Config, config
from .loggers import init_logger

init_logger()

__all__ = ["config", "Config"]

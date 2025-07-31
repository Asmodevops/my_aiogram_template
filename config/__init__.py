from .loggers import init_logger
from .config_reader import Config, config

init_logger()

__all__ = ["config", "Config"]

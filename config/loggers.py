import logging
import logging.handlers
import sys
from collections.abc import MutableMapping


class ColoredFormatter(logging.Formatter):
    COLORS: MutableMapping[int, str] = {
        logging.DEBUG: "\033[34m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[1;31m",
    }
    RESET = "\033[0m"

    def __init__(self, fmt: str, datefmt: str | None = None) -> None:
        super().__init__(fmt, datefmt)

    def format(self, record) -> str:
        color: str = self.COLORS.get(record.levelno, self.RESET)
        record.levelname = f"{color}{record.levelname}"
        record.msg = f"{record.msg}{self.RESET}"
        return super().format(record)


async def init_logger() -> None:
    """
    Initialize the logger with a console handler and a specific format.

    The logger will output log messages to the standard error stream with the following format:
    [TIME - LEVEL - FILE - FUNCTION - LINE] - MESSAGE

    The log level is set to INFO, which means that all messages with a level of INFO or higher
    will be output.
    """
    console_handler = logging.StreamHandler(stream=sys.stderr)
    console_handler.setFormatter(
        ColoredFormatter(
            "[%(asctime)s] - #%(levelname)-8s %(filename)s:%(lineno)d - %(name)s - %(message)s",
            datefmt="%H:%M:%S",
        )
    )

    logger: logging.Logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)

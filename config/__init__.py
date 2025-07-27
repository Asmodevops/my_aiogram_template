from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .config_reader import Config
from .loggers import init_logger

config: Config = Config.load_config()
bot = Bot(
    token=config.tg_bot.token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

__all__ = [bot, config, init_logger]

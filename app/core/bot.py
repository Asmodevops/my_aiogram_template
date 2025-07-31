import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.core.faststream import broker, publisher
from app.core.storage import storage
from app.services.scheduler import redis_source
from config import config

logger = logging.getLogger(__name__)

bot = Bot(
    token=config.tg_bot.token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher(
    storage=storage,
    broker=broker,
    publisher=publisher,
    config=config,
    redis_source=redis_source
)

import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.core.faststream import broker
from app.core.storage import storage
from app.services.scheduler import redis_source, taskiq_broker
from config import config

logger = logging.getLogger(__name__)

bot = Bot(
    token=config.tg_bot.token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher(
    storage=storage,
    broker=broker,
    config=config,
    redis_source=redis_source
)


@dp.startup()
async def setup_taskiq(bot: Bot, *_args, **_kwargs):
    if not taskiq_broker.is_worker_process:
        logging.info("Setting up taskiq")
        await taskiq_broker.startup()


@dp.shutdown()
async def shutdown_taskiq(bot: Bot, *_args, **_kwargs):
    if not taskiq_broker.is_worker_process:
        logging.info("Shutting down taskiq")
        await taskiq_broker.shutdown()

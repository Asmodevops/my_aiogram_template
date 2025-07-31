import logging

from aiogram import Bot, Dispatcher

from app.core.faststream import broker, publisher
from app.core.storage import storage
from app.services.scheduler import redis_source, taskiq_broker
from config import config

logger = logging.getLogger(__name__)

dp = Dispatcher(
    storage=storage,
    broker=broker,
    publisher=publisher,
    config=config,
    redis_source=redis_source
)

@dp.startup()
async def setup_taskiq(bot: Bot, *_args, **_kwargs):
    await broker.start()
    if not taskiq_broker.is_worker_process:
        logging.info("Setting up taskiq")
        await taskiq_broker.startup()

@dp.shutdown()
async def shutdown_taskiq(bot: Bot, *_args, **_kwargs):
    await broker.close()
    if not taskiq_broker.is_worker_process:
        logging.info("Shutting down taskiq")
        await taskiq_broker.shutdown()

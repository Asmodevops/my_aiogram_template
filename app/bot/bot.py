import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import Redis, RedisStorage
from aiogram.methods import DeleteWebhook
from aiogram_dialog import setup_dialogs
from faststream.nats import NatsBroker
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.bot.handlers import get_routers
from app.bot.handlers.admin import router as admin_router
from app.bot.keyboards import set_main_menu
from app.bot.middlewares import *
from app.faststream import get_stream_routers
from config import bot, config, init_logger

logger = logging.getLogger(__name__)


async def main():
    init_logger()

    logger.info("Create db engine...")
    engine = create_async_engine(url=str(config.pg_db.dsn), echo=config.pg_db.is_echo)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    logger.info("Create redis storage...")
    storage = RedisStorage(
        redis=Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
            password=config.redis.password.get_secret_value()
        ),
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )

    logger.info("Create faststream broker...")
    broker = NatsBroker(servers=str(config.nats.server))
    broker.include_routers(*get_stream_routers())

    logger.info("Including routers...")
    dp = Dispatcher(
        storage=storage,
        broker=broker,
        config=config
    )
    dp.include_routers(*get_routers())

    logger.info("Including middlewares...")
    dp.message.middleware(ThrottlingMiddleware(throttle_time=config.tg_bot.throttling_time))
    dp.update.middleware(DbSessionMiddleware(session_maker))
    dp.update.middleware(RepositoryMiddleware())
    dp.update.middleware(UserSaverMiddleware())
    admin_router.message.middleware(IsAdminMiddleware())
    admin_router.callback_query.middleware(IsAdminMiddleware())

    logger.info("Setup dialogs...")
    setup_dialogs(dp)

    logger.info("Set main menu...")
    await set_main_menu(bot)

    logger.info("Delete webhooks...")
    await bot(DeleteWebhook(drop_pending_updates=True))

    async with broker:
        logger.info("Starting Faststream broker...")
        await broker.start()
        logger.info("Starting Bot...")
        await dp.start_polling(bot)

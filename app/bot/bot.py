import logging

from aiogram import Bot
from aiogram.methods import DeleteWebhook
from aiogram_dialog import setup_dialogs

from app.bot.handlers import get_routers
from app.bot.handlers.admin import router as admin_router
from app.bot.keyboards import set_main_menu
from app.bot.middlewares import (
    DbSessionMiddleware,
    IsAdminMiddleware,
    PublisherMiddleware,
    RepositoryMiddleware,
    ThrottlingMiddleware,
    UserSaverMiddleware
)
from app.core import (
    bot,
    broker,
    dp,
    session_maker,
    storage
)
from app.services.faststream import get_stream_routers
from app.services.scheduler import taskiq_broker, redis_source
from config import config

logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting bot...")

    dp.workflow_data.update(
        storage=storage,
        broker=broker,
        config=config,
        redis_source=redis_source
    )

    logger.info("Including bot routers...")
    dp.include_routers(*get_routers())

    logger.info("Including faststream routers...")
    broker.include_routers(*get_stream_routers())

    logger.info("Including middlewares...")
    dp.message.middleware(ThrottlingMiddleware(throttle_time=config.tg_bot.throttling_time))
    dp.update.middleware(DbSessionMiddleware(session_maker))
    dp.update.middleware(PublisherMiddleware(broker))
    dp.update.middleware(RepositoryMiddleware())
    dp.update.middleware(UserSaverMiddleware())
    admin_router.message.middleware(IsAdminMiddleware())
    admin_router.callback_query.middleware(IsAdminMiddleware())

    @dp.startup()
    async def setup_taskiq(bot: Bot, *_args, **_kwargs):
        logging.info("Start up faststream broker...")
        await broker.start()
        if not taskiq_broker.is_worker_process:
            logging.info("Start up taskiq broker...")
            await taskiq_broker.startup()

    @dp.shutdown()
    async def shutdown_taskiq(bot: Bot, *_args, **_kwargs):
        logging.info("Shutting down faststream broker...")
        await broker.close()
        if not taskiq_broker.is_worker_process:
            logging.info("Shutting down taskiq broker...")
            await taskiq_broker.shutdown()

    logger.info("Setup dialogs...")
    setup_dialogs(dp)

    logger.info("Set main menu...")
    await set_main_menu(bot)

    logger.info("Delete webhooks...")
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

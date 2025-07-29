import asyncio
import logging

from aiogram.methods import DeleteWebhook
from aiogram_dialog import setup_dialogs
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.bot.handlers import get_routers
from app.bot.handlers.admin import router as admin_router
from app.bot.keyboards import set_main_menu
from app.bot.middlewares import *
from app.core.bot import dp, bot
from app.core.faststream import broker, app
from app.services.faststream import get_stream_routers
from app.services.scheduler import taskiq_broker
from config.config_reader import config

logger = logging.getLogger(__name__)


async def main():
    logger.info("Create db engine...")
    engine = create_async_engine(url=str(config.pg_db.dsn), echo=config.pg_db.is_echo)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    logger.info("Including faststream routers...")
    broker.include_routers(*get_stream_routers())

    logger.info("Including bot routers...")
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

    try:
        await asyncio.gather(
            app.start(),
            dp.start_polling(bot)
        )
    except Exception as e:
        logger.exception(e)
    finally:
        await taskiq_broker.shutdown()
        logger.info("Connection to taskiq-broker closed")
        await app.stop()
        logger.info("Connection to Faststream closed")

import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import Redis, RedisStorage
from aiogram.methods import DeleteWebhook

from aiogram_dialog import setup_dialogs
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.bot.handlers import get_routers
from app.bot.handlers.admin import router as admin_router
from app.bot.keyboards.side_menu import set_main_menu
from app.bot.middlewares.is_admin import IsAdminMiddleware
from app.bot.middlewares.repository import RepositoryMiddleware
from app.bot.middlewares.session import DbSessionMiddleware
from app.bot.middlewares.user import UserSaverMiddleware
from config.config_reader import Config
from config.loggers import init_logger

logger = logging.getLogger(__name__)


async def main():
    await init_logger()

    logger.info("Starting Bot...")

    config: Config = Config.load_config()

    engine = create_async_engine(url=str(config.pg_db.dsn), echo=config.pg_db.is_echo)
    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    storage = RedisStorage(
        redis=Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
        ),
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )

    bot = Bot(
        token=config.tg_bot.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher(storage=storage)
    dp.include_routers(*get_routers())

    dp.update.middleware(DbSessionMiddleware(Sessionmaker))
    dp.update.middleware(RepositoryMiddleware())
    dp.update.middleware(UserSaverMiddleware())
    admin_router.message.middleware(IsAdminMiddleware())
    admin_router.callback_query.middleware(IsAdminMiddleware())

    setup_dialogs(dp)

    await set_main_menu(bot)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot, config=config)

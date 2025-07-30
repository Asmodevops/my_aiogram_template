from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import Redis, RedisStorage

from config import config

storage = RedisStorage(
    redis=Redis(
        host=config.redis.host,
        port=config.redis.port,
        db=config.redis.db,
        password=config.redis.password.get_secret_value()
    ),
    key_builder=DefaultKeyBuilder(with_destiny=True),
)

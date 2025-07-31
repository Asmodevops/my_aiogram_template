import logging

import taskiq_aiogram
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import PullBasedJetStreamBroker
from taskiq_redis import RedisScheduleSource

from config import config

logger = logging.getLogger(__name__)

logger.info("Create taskiq broker...")
taskiq_broker = PullBasedJetStreamBroker(
    servers=str(config.nats.server),
    queue="taskiq_tasks"
)

logger.info("Create redis storage...")
redis_source = RedisScheduleSource(
    url=f"redis://:{config.redis.password.get_secret_value()}@{config.redis.host}:{config.redis.port}"
)

scheduler = TaskiqScheduler(taskiq_broker, [redis_source, LabelScheduleSource(taskiq_broker)])

taskiq_aiogram.init(
    taskiq_broker,
    "app.core.dispatcher:dp",
    "app.core.bot:bot"
)

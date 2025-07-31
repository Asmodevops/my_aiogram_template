import logging

from faststream.nats import NatsBroker

from app.services.faststream import Publisher
from config import config

logger = logging.getLogger(__name__)

logger.info("Create faststream broker...")
broker = NatsBroker(servers=str(config.nats.server))

logger.info("Create faststream app...")

publisher: Publisher = Publisher(
    broker=broker,
    delayed_sub=config.delayed_consumer.subject,
    delayed_stream=config.delayed_consumer.stream
)

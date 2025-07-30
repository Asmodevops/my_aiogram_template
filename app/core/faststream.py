import logging

from faststream import FastStream
from faststream.nats import NatsBroker

from config import config

logger = logging.getLogger(__name__)

logger.info("Create faststream broker...")
broker = NatsBroker(servers=str(config.nats.server))

logger.info("Create faststream app...")
app = FastStream(broker)

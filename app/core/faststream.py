from faststream.nats import NatsBroker

from config import config

broker = NatsBroker(servers=str(config.nats.server))

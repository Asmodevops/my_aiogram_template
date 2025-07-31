from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from faststream.nats import NatsBroker

from app.services.faststream import Publisher
from config import Config


class PublisherMiddleware(BaseMiddleware):
    def __init__(self, broker: NatsBroker):
        self.broker = broker

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        config: Config = data.get("config")
        publisher: Publisher = Publisher(
            broker=self.broker,
            delayed_sub=config.delayed_consumer.subject,
            delayed_stream=config.delayed_consumer.stream
        )
        data.update(
            {
                "publisher": publisher
            }
        )
        return await handler(event, data)

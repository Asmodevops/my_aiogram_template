from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, User
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, throttle_time: float):
        self.cache = TTLCache(maxsize=10_000, ttl=throttle_time)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")
        if user.id in self.cache:
            return
        self.cache[user.id] = None
        return await handler(event, data)

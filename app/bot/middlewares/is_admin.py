from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from config.config_reader import Config


class IsAdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")
        config: Config = data.get("config")
        if user is not None:
            if user.id == config.basic_ids.admin_id:
                return await handler(event, data)
        return None

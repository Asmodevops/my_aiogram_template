from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from typing import Callable, Dict, Any, Awaitable

from app.infrastructure.database.repository import UserRepository


class UserSaverMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        tg_user: User = data.get("event_from_user")
        if tg_user:
            user_repo: UserRepository = data.get("user_repo")

            user = await user_repo.create_user(
                telegram_id=tg_user.id,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                full_name=tg_user.full_name,
                username=tg_user.username,
            )

            data["user"] = user

        return await handler(event, data)

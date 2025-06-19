from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from pydantic import ValidationError

from app.bot.repository.users import UserRepository
from app.bot.schemas.user import UserSchema

router = Router(name="admin router")


@router.message(Command(commands=["test"]))
async def cmd_test(message: Message, user_repo: UserRepository):
    raw_user = await user_repo.get_by_id(
        id=1, return_fields=["telegram_id", "full_name", "username"]
    )

    if not raw_user:
        await message.answer("User not found")
        return

    try:
        user = UserSchema.model_validate(raw_user)
    except ValidationError as e:
        await message.answer(f"Invalid user data: {e}")
        return

    await message.answer(
        f"User info:\n"
        f"ID: {user.telegram_id}\n"
        f"Name: {user.full_name}\n"
        f"Username: @{user.username}"
    )

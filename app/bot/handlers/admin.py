from datetime import datetime, timedelta

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from faststream.nats import NatsBroker

from app.bot.services.admin_services import UserServices
from app.infrastructure.database.repository import UserRepository
from config import Config

router = Router(name="admin router")


@router.message(Command(commands=["test"]))
async def cmd_test(message: Message, user_repo: UserRepository, broker: NatsBroker, config: Config):
    user_services = UserServices(user_repo)
    user = await user_services.get_validated_user_by_id(1)
    if not user:
        await message.answer("User not found or invalid data")
        return
    if not broker.running:
        await message.answer(
            f"User info:\n"
            f"ID: {user.telegram_id}\n"
            f"Name: {user.full_name}\n"
            f"Username: @{user.username}"
        )
        return

    await message.answer(
        f"Сообщение с вашими данными придет через 5 секунд..."
    )

    delay = 5
    msg_data = {
        'delayed_msg_timestamp': datetime.now() + timedelta(seconds=delay),
        'msg': f"User info:\nID: {user.telegram_id}\nName: {user.full_name}\nUsername: @{user.username}",
        'user_id': message.from_user.id
    }
    await broker.publish(
        message=msg_data,
        subject=config.delayed_consumer.subject,
        stream=config.delayed_consumer.stream
    )

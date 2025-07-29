import asyncio
from datetime import datetime, timezone, timedelta

from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from faststream.nats import NatsBroker
from taskiq import ScheduledTask
from taskiq_redis import RedisScheduleSource

from app.bot.enums import Action
from app.bot.services.admin_services import UserServices
from app.infrastructure.database.repository import UserRepository
from app.services.scheduler import dynamic_periodic_task, scheduled_task, simple_task
from config import Config

router = Router(name="general router")


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Это шаблон Telegram бота от asmodev.")


@router.message(Command(commands=["test"]))
async def cmd_test(
        message: Message,
        user_repo: UserRepository,
        broker: NatsBroker,
        config: Config
):
    user_services = UserServices(user_repo)
    user = await user_services.get_validated_user_by_telegram_id(telegram_id=message.from_user.id)
    await message.answer(
        f"Сообщение с вашими данными придет через 5 секунд..."
    )
    if not broker.running:
        await asyncio.sleep(5)
        await message.answer(
            f"User info:\n"
            f"ID: {user.telegram_id}\n"
            f"Name: {user.full_name}\n"
            f"Username: @{user.username}"
        )
        return

    delay = 5
    msg_data = {
        'action_type': Action.POST,
        'delayed_msg_timestamp': datetime.now() + timedelta(seconds=delay),
        'msg': f"User info:\nID: {user.telegram_id}\nName: {user.full_name}\nUsername: @{user.username}",
        'chat_id': message.chat.id
    }
    await broker.publish(
        message=msg_data,
        subject=config.delayed_consumer.subject,
        stream=config.delayed_consumer.stream
    )


@router.message(Command(commands=["del"]))
async def cmd_test(
        message: Message,
        broker: NatsBroker,
        config: Config,
        bot: Bot
):
    msg: Message = await message.answer(
        f"Это сообщение удалится через 3 секунды" + " брокером сообщений" if broker.running else ""
    )
    if not broker.running:
        await asyncio.sleep(3)
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id,
        )
        return

    delay = 3
    msg_data = {
        'action_type': Action.DELETE,
        'delayed_msg_timestamp': datetime.now() + timedelta(seconds=delay),
        'msg_id': msg.message_id,
        'chat_id': message.chat.id
    }
    await broker.publish(
        message=msg_data,
        subject=config.delayed_consumer.subject,
        stream=config.delayed_consumer.stream
    )


@router.message(Command("simple"))
async def task_handler(
        message: Message,
        redis_source: RedisScheduleSource
) -> None:
    await simple_task.kiq()
    await message.answer(
        text="Простая задача"
    )


@router.message(Command("periodic"))
async def dynamic_periodic_task_handler(
        message: Message,
        state: FSMContext,
        redis_source: RedisScheduleSource,
) -> None:
    periodic_task: ScheduledTask = await dynamic_periodic_task.schedule_by_cron(
        source=redis_source, cron="* * * * *"
    )

    data: dict = await state.get_data()
    if data.get("periodic_tasks") is None:
        data["periodic_tasks"] = []

    data["periodic_tasks"].append(periodic_task.schedule_id)

    await state.set_data(data)
    await message.answer(text="Периодическая задача запланирована")


@router.message(Command("del_periodic"))
async def delete_all_periodic_tasks_handler(
        message: Message,
        state: FSMContext,
        redis_source: RedisScheduleSource,
) -> None:
    data = await state.get_data()
    if data.get("periodic_tasks") is None:
        await message.answer(text="Нет периодических запланированных задач")
    else:
        for task_id in data.get("periodic_tasks"):
            await redis_source.delete_schedule(task_id)
        await message.answer(text="Периодическая задача удалена")


@router.message(Command("delay"))
async def delay_task_handler(
        message: Message,
        redis_source: RedisScheduleSource
) -> None:
    await scheduled_task.schedule_by_time(
        source=redis_source, time=datetime.now(timezone.utc) + timedelta(seconds=5)
    )
    await message.answer("Разовая задача запланирована")

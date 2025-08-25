import asyncio
from datetime import datetime, timezone, timedelta

from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from faststream.nats import NatsBroker
from taskiq import ScheduledTask
from taskiq_redis import RedisScheduleSource

from app.bot.lexicon import lexicon
from app.bot.services import UserServices
from app.infrastructure.database.repository import UserRepository
from app.services.faststream import Publisher
from app.services.scheduler import dynamic_periodic_task, scheduled_task, simple_task

router = Router(name="general router")


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text=lexicon.start
    )


@router.message(Command(commands=["test"]))
async def cmd_test(
        message: Message,
        user_repo: UserRepository,
        broker: NatsBroker,
        publisher: Publisher
):
    user_services = UserServices(user_repo)
    user = await user_services.get_validated_user_by_telegram_id(telegram_id=message.from_user.id)
    await message.answer(
        text=lexicon.test
    )
    if not broker.running:
        await asyncio.sleep(5)
        await message.answer(
            text=lexicon.user_info.format(
                telegram_id=user.telegram_id,
                full_name=user.full_name,
                username=user.username
            )
        )
        return

    delay = 5
    await publisher.delayed_send_message(
        message=f"User info:\nID: {user.telegram_id}\nName: {user.full_name}\nUsername: @{user.username}",
        chat_id=message.chat.id,
        time_to_action=datetime.now() + timedelta(seconds=delay),
    )


@router.message(Command(commands=["del"]))
async def cmd_del(
        message: Message,
        broker: NatsBroker,
        publisher: Publisher,
        bot: Bot
):
    msg: Message = await message.answer(
        text=lexicon.del_
    )
    if not broker.running:
        await asyncio.sleep(3)
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id,
        )
        return

    delay = 3
    await publisher.delayed_delete_message(
        message_id=msg.message_id,
        chat_id=msg.chat.id,
        time_to_action=datetime.now() + timedelta(seconds=delay)
    )


@router.message(Command("simple"))
async def task_handler(
        message: Message
) -> None:
    await simple_task.kiq()
    await message.answer(
        text=lexicon.simple
    )


@router.message(Command("periodic"))
async def dynamic_periodic_task_handler(
        message: Message,
        state: FSMContext,
        redis_source: RedisScheduleSource,
) -> None:
    periodic_task: ScheduledTask = await dynamic_periodic_task.schedule_by_cron(
        source=redis_source, cron="*/2 * * * *"
    )

    data: dict = await state.get_data()
    if data.get("periodic_tasks") is None:
        data["periodic_tasks"] = []

    data["periodic_tasks"].append(periodic_task.schedule_id)

    await state.set_data(data)
    await message.answer(
        text=lexicon.periodic
    )


@router.message(Command("del_periodic"))
async def delete_all_periodic_tasks_handler(
        message: Message,
        state: FSMContext,
        redis_source: RedisScheduleSource,
) -> None:
    data = await state.get_data()
    if data.get("periodic_tasks") is None:
        await message.answer(
            text=lexicon.no_periodic
        )
    else:
        for task_id in data.get("periodic_tasks"):
            await redis_source.delete_schedule(task_id)
        await message.answer(
            text=lexicon.del_periodic
        )


@router.message(Command("delay"))
async def delay_task_handler(
        message: Message,
        redis_source: RedisScheduleSource
) -> None:
    await scheduled_task.schedule_by_time(
        source=redis_source, time=datetime.now(timezone.utc) + timedelta(seconds=5)
    )
    await message.answer(
        text=lexicon.delay
    )


@router.message(Command("help"))
async def process_help_command(
        message: Message,
) -> None:
    await message.answer(
        text=lexicon.help
    )

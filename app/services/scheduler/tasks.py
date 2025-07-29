import time

from aiogram import Bot
from taskiq import TaskiqDepends

from app.services.scheduler.taskiq_broker import taskiq_broker
from config import config


@taskiq_broker.task
async def simple_task(bot: Bot = TaskiqDepends()):
    await bot.send_message(
        chat_id=config.basic_ids.admin_id,
        text="Это простая задача без расписания"
    )


@taskiq_broker.task(task_name="periodic_task", schedule=[{"cron": "* * * * *"}])
async def periodic_task(bot: Bot = TaskiqDepends()):
    await bot.send_message(
        chat_id=config.basic_ids.admin_id,
        text=f"{time.strftime('%H:%M:%S', time.localtime(time.time()))}: Это периодическая задача, выполняющаяся раз в минуту"
    )


@taskiq_broker.task
async def dynamic_periodic_task(bot: Bot = TaskiqDepends()):
    await bot.send_message(
        chat_id=config.basic_ids.admin_id,
        text=f"{time.strftime('%H:%M:%S', time.localtime(time.time()))}: Это динамически запланированная периодическая задача"
    )


@taskiq_broker.task
async def scheduled_task(bot: Bot = TaskiqDepends()):
    await bot.send_message(
        chat_id=config.basic_ids.admin_id,
        text=f"{time.strftime('%H:%M:%S', time.localtime(time.time()))}: Это запланированная разовая задача"
    )

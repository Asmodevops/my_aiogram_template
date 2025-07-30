import time

from aiogram import Bot
from taskiq import TaskiqDepends

from app.services.scheduler.taskiq_broker import taskiq_broker
from app.services.scheduler.taskiq_lexicon import taskiq_lexicon
from config import config


@taskiq_broker.task
async def simple_task(bot: Bot = TaskiqDepends()):
    await bot.send_message(
        chat_id=config.basic_ids.admin_id,
        text=taskiq_lexicon.simple_task
    )


@taskiq_broker.task(task_name="periodic_task", schedule=[{"cron": "* * * * *"}])
async def periodic_task(bot: Bot = TaskiqDepends()):
    await bot.send_message(
        chat_id=config.basic_ids.admin_id,
        text=taskiq_lexicon.periodic_task.format(
            time=time.strftime('%H:%M:%S', time.localtime(time.time()))
        )
    )


@taskiq_broker.task
async def dynamic_periodic_task(bot: Bot = TaskiqDepends()):
    await bot.send_message(
        chat_id=config.basic_ids.admin_id,
        text=taskiq_lexicon.dynamic_periodic_task.format(
            time=time.strftime('%H:%M:%S', time.localtime(time.time()))
        )
    )


@taskiq_broker.task
async def scheduled_task(bot: Bot = TaskiqDepends()):
    await bot.send_message(
        chat_id=config.basic_ids.admin_id,
        text=taskiq_lexicon.scheduled_task.format(
            time=time.strftime('%H:%M:%S', time.localtime(time.time()))
        )
    )

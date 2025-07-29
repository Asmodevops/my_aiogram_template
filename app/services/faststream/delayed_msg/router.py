from datetime import datetime

from faststream.nats import JStream, NatsRouter, PullSub
from faststream.nats.annotations import NatsMessage

from app.bot.enums import Action
from app.core.bot import bot
from config.config_reader import config

router = NatsRouter()


@router.subscriber(
    subject=config.delayed_consumer.subject,
    stream=JStream(name=config.delayed_consumer.stream),
    durable=config.delayed_consumer.durable,
    pull_sub=PullSub()
)
async def delayed_send_message(
    body: dict,
    msg: NatsMessage,
):
    if body.get('action_type') == Action.POST:
        sent_time = datetime.fromisoformat(body.get('delayed_msg_timestamp'))

        if sent_time >= datetime.now():
            delay = (sent_time - datetime.now()).total_seconds()
            await msg.nack(delay=delay)
        else:
            await bot.send_message(
                chat_id=body.get("chat_id"),
                text=body.get("msg")
            )
            await msg.ack()
    elif body.get('action_type') == Action.DELETE:
        sent_time = datetime.fromisoformat(body.get('delayed_msg_timestamp'))

        if sent_time >= datetime.now():
            delay = (sent_time - datetime.now()).total_seconds()
            await msg.nack(delay=delay)
        else:
            await bot.delete_message(
                chat_id=body.get("chat_id"),
                message_id=body.get("msg_id")
            )
            await msg.ack()

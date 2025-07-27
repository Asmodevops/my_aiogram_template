from datetime import datetime

from faststream.nats import JStream, NatsRouter
from faststream.nats.annotations import NatsMessage

from config import bot, config

router = NatsRouter()


@router.subscriber(
    subject=config.delayed_consumer.subject,
    stream=JStream(name=config.delayed_consumer.stream),
    durable=config.delayed_consumer.durable,
)
async def start_handler(
    body: dict,
    msg: NatsMessage,
):
    sent_time = datetime.fromisoformat(body.get('delayed_msg_timestamp'))

    if sent_time >= datetime.now():
        delay = (sent_time - datetime.now()).total_seconds()
        await msg.nack(delay=delay)
    else:
        await bot.send_message(
            chat_id=body.get("user_id"),
            text=body.get("msg")
        )
        await msg.ack()

from datetime import datetime
from typing import Any

from faststream.nats import NatsBroker

from app.bot.enums import Action


class Publisher:
    def __init__(
            self,
            broker: NatsBroker,
            delayed_sub: str,
            delayed_stream: str
    ):
        self.broker = broker
        self.delayed_sub = delayed_sub
        self.delayed_stream = delayed_stream

    async def delayed_send_message(
            self,
            message: str,
            chat_id: int,
            time_to_action: datetime
    ):
        msg_data = {
            'action_type': Action.POST,
            'delayed_msg_timestamp': time_to_action,
            'msg': message,
            'chat_id': chat_id
        }
        await self._publish_message(
            data=msg_data,
            sub_chat_id=chat_id
        )

    async def delayed_delete_message(
            self,
            message_id: int,
            chat_id: int,
            time_to_action: datetime
    ):
        msg_data = {
            'action_type': Action.DELETE,
            'delayed_msg_timestamp': time_to_action,
            'msg_id': message_id,
            'chat_id': chat_id
        }
        await self._publish_message(
            data=msg_data,
            sub_chat_id=chat_id
        )

    async def _publish_message(self, data: dict[str, Any], sub_chat_id: str | int):
        await self.broker.publish(
            message=data,
            subject=self.delayed_sub.replace('*', str(sub_chat_id)),
            stream=self.delayed_stream
        )

from functools import cached_property
from typing import Any

from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels_redis.core import RedisChannelLayer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import Room


@database_sync_to_async
def get_room(room_code: str) -> Room:
    try:
        return Room.objects.get(pk=room_code)
    except ObjectDoesNotExist as err:
        raise DenyConnection("Invalid room code") from err


class RoomConsumer(AsyncJsonWebsocketConsumer):
    channel_layer: RedisChannelLayer

    @cached_property
    def room_code(self) -> str:
        return self.scope["url_route"]["kwargs"]["room_code"]  # type: ignore

    @cached_property
    def group_name(self) -> str:
        return f"room_{self.room_code}"

    @property
    def user(self) -> User:
        return self.scope["user"]  # type: ignore

    async def connect(self) -> None:
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, _code: Any) -> None:
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content: dict) -> None:
        ...
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": content,
                "username": self.user.username,
                "room": self.room_code,
            },
        )

    async def chat_message(self, event: Any) -> None:
        await self.send_json(event)

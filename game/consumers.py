import enum
from functools import cached_property
from typing import Any

from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels_redis.core import RedisChannelLayer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from game.logic import handlers as h
from game.serializers.room import RoomSerializer
from .models import Room


class ActionType(enum.StrEnum):
    unknown = enum.auto()
    update_player_name = enum.auto()


actions_types: dict[ActionType, h.HandlerProtocol] = {
    ActionType.update_player_name: h.update_user,
    ActionType.unknown: h.handle_unknown_type,
}


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
        action = actions_types.get(content["type"], actions_types[ActionType.unknown])
        async_acion = database_sync_to_async(action)
        result = await async_acion(self.user, content["message"])
        room = await get_room(self.room_code)
        async_serializer = database_sync_to_async(RoomSerializer)
        serializer = await async_serializer(room)
        print(serializer.data)

        # await self.channel_layer.group_send(
        #     self.group_name,
        #     {
        #         "type": "send_message_to_group_member",
        #         "message": serializer.data,
        #     },
        # )

    async def send_message_to_group_member(self, event: Any) -> None:
        await self.send_json(event["message"])

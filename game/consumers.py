import enum
from functools import cached_property
from typing import Any

from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels_redis.core import RedisChannelLayer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Prefetch
from pydantic import ValidationError

from . import handlers as h
from . import models as m
from .exceptions import GameError
from .models_pydantic.room import Room


class ActionType(enum.StrEnum):
    unknown = enum.auto()
    update_player_name = enum.auto()
    choose_pawn = enum.auto()
    leave_room = enum.auto()
    come_up_with_an_association = enum.auto()


actions_types: dict[ActionType, h.HandlerProtocol] = {
    ActionType.update_player_name: h.handle_user_update,
    ActionType.unknown: h.handle_unknown_type,
    ActionType.choose_pawn: h.handle_chooese_pawn,
    ActionType.leave_room: h.handle_leave_room,
    ActionType.come_up_with_an_association: h.handle_come_up_with_an_association,
}


@database_sync_to_async
def get_room(room_code: str) -> m.Room:
    try:
        room = (
            m.Room.objects.prefetch_related(
                Prefetch("pawns", queryset=m.Pawn.objects.order_by("id"))
            )
            .prefetch_related("pawns__color")
            .prefetch_related("pawns__player")
            .prefetch_related("pawns__player__user")
            .prefetch_related(
                Prefetch(
                    "pawns__room_card",
                    queryset=m.RoomCard.objects.filter(is_deleted=False).order_by("id"),
                )
            )
            .prefetch_related("pawns__room_card__card")
            .get(pk=room_code)
        )

    except ObjectDoesNotExist as err:
        raise DenyConnection("Invalid room code") from err
    else:
        return room


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
        type_ = content["type"] if content["type"] in actions_types else ActionType.unknown
        action = actions_types[type_]
        async_acion = database_sync_to_async(action)

        try:
            _result = await async_acion(content["message"], self.user)
        except ValidationError as err:
            await self.send_json({"type": "ValidationError", "message": str(err)})
            return
        except ObjectDoesNotExist as err:
            await self.send_json({"type": "DoesNotExist", "message": str(err)})
            return
        except GameError as err:
            await self.send_json({"type": "GameError", "message": str(err)})
            return

        room = await get_room(self.room_code)
        room_ = Room.model_validate(room)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_message_to_group_member",
                "message": {"type": type_, "room": room_.model_dump()},
            },
        )

    async def send_message_to_group_member(self, event: Any) -> None:
        await self.send_json(event["message"])

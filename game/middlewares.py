from typing import Any

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.security.websocket import WebsocketDenier
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from game.models.room import Room


@database_sync_to_async
def get_user(token_key: str) -> User | None:
    try:
        token = Token.objects.get(key=token_key)
        return token.user  # type: ignore
    except Token.DoesNotExist:
        return None


@database_sync_to_async
def get_room(room_code: str) -> Room | None:
    try:
        return Room.objects.get(code=room_code)
    except Room.DoesNotExist:
        return None


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner: Any):
        super().__init__(inner)

    async def __call__(self, scope: dict, receive: Any, send: Any) -> Any:
        token = scope["query_string"].decode().split("=")[-1]

        user = await get_user(token) if token else None
        if not user:
            denier = WebsocketDenier()
            return await denier(scope, receive, send)

        scope["user"] = user
        return await super().__call__(scope, receive, send)


class RoomMiddleware(BaseMiddleware):
    def __init__(self, inner: Any):
        super().__init__(inner)

    async def __call__(self, scope: dict, receive: Any, send: Any) -> Any:
        room_code = scope["path"].split("/")[3]
        room = await get_room(room_code) if room_code else None

        if not room:
            denier = WebsocketDenier()
            return await denier(scope, receive, send)
        return await super().__call__(scope, receive, send)

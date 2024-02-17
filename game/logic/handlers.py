
from typing import Any, Protocol

from django.contrib.auth.models import User

class HandlerProtocol(Protocol):
    def __call__(self, user: User, data: dict) -> Any:
        pass

def handle_unknown_type(*args: Any, **kwargs: Any) -> dict:
    return {"message":"Event type unknown"}

def update_user(user: User, data: dict) -> dict:
    user.player.name = data["player_name"]
    user.player.save()
    return {"success": True}

from typing import Any, Protocol

from django.contrib.auth.models import User


class HandlerProtocol(Protocol):
    def __call__(self, data: Any, user: User) -> None:
        pass


def handle_unknown_type(*args: Any, **kwargs: Any) -> None:
    pass

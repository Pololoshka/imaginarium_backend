"""
ASGI config for src project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import game.routing
from game.middlewares import RoomExistsMiddleware, TokenAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": RoomExistsMiddleware(
            TokenAuthMiddleware(URLRouter(game.routing.websocket_urlpatterns))
        ),
    }
)

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_asgi_app = get_asgi_application()

# Import po ustawieniu DJANGO_SETTINGS_MODULE
from events.consumers import EventConsumer  # noqa

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter(
            [
                path("ws/events/<int:event_id>/", EventConsumer.as_asgi()),
            ]
        ),
    }
)

from datetime import datetime, timedelta

import pytest
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from config.asgi import application
from django.utils import timezone
from events.models import Event
from tests.utils import unique_email
from users.models import CustomUser
import pytest
pytestmark = pytest.mark.django_db(transaction=True)


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_ws_connects_ok():
    organizer = await database_sync_to_async(CustomUser.objects.create_user)(
        email=unique_email(), password="pass"
    )

    now = timezone.now()

    event = await database_sync_to_async(Event.objects.create)(
        title="WS test",
        location="Online",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=1, hours=2),
        seats_limit=10,
        status="published",
        organizer=organizer,
    )

    communicator = WebsocketCommunicator(application, f"/ws/events/{event.id}/")

    connected, _ = await communicator.connect()

    assert connected is True

    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_ws_metrics_broadcasts_json():
    communicator = WebsocketCommunicator(application, "/ws/events/1/")
    connected, _ = await communicator.connect()
    assert connected, "Nie udało się połączyć z WebSocketem"

    response = await communicator.receive_json_from()

    expected_keys = {"event_id", "confirmed_count", "pending_count", "checked_in_count"}
    assert expected_keys.issubset(response.keys()), f"Niepoprawny format metryk: {response}"

    await communicator.disconnect()
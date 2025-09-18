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
@pytest.mark.django_db
async def test_ws_metrics_broadcasts_json():

    organizer = await sync_to_async(CustomUser.objects.create_user)(
        email=unique_email(), password="pass"
    )

    now = timezone.now()
    event = await sync_to_async(Event.objects.create)(
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

    channel_layer = get_channel_layer()
    payload = {
        "type": "metrics",
        "event_id": event.id,
        "confirmed_count": 1,
        "pending_count": 2,
        "checked_in_count": 0,
        "spots_left": 5,
    }

    # Act – wyślij do grupy, którą consumer subskrybuje po connect()
    await channel_layer.group_send(
        f"event_{event.id}",
        {"type": "event.metrics", "payload": payload},
    )

    data = await communicator.receive_json_from(timeout=2)

    # Assert
    assert data == payload

    await communicator.disconnect()

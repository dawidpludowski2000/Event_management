from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone
from events.models import Event
from reservations.models import Reservation
from rest_framework.test import APIClient
from tests.utils import unique_email
from users.models import CustomUser


@pytest.mark.django_db
def test_cancel_event_twice_second_call_200_no_changes():
    organizer = CustomUser.objects.create_user(email=unique_email(), password="pass")

    u1 = CustomUser.objects.create_user(email="u1@example.com", password="pass")
    u2 = CustomUser.objects.create_user(email="u2@example.com", password="pass")
    u3 = CustomUser.objects.create_user(email="u3@example.com", password="pass")

    now = timezone.now()

    event = Event.objects.create(
        title="Test",
        location="Online",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=2, hours=2),
        seats_limit=2,
        status="published",
        organizer=organizer,
    )

    client = APIClient()

    client.force_authenticate(user=organizer)

    Reservation.objects.create(event=event, user=u1, status="pending")
    Reservation.objects.create(event=event, user=u2, status="confirmed")
    Reservation.objects.create(event=event, user=u3, status="rejected")

    resp = client.post(f"/api/events/organizer/{event.id}/cancel/")

    assert resp.status_code == 200
    event.refresh_from_db()

    assert event.status == "cancelled"

    assert Reservation.objects.filter(event=event, status="pending").count() == 0
    assert Reservation.objects.filter(event=event, status="confirmed").count() == 0
    assert Reservation.objects.filter(event=event, status="rejected").count() == 3

    with patch("events.views.event_cancel.broadcast_event_metrics"):
        client.post(f"/api/events/organizer/{event.id}/cancel/")

    assert resp.status_code == 200
    event.refresh_from_db()

    assert event.status == "cancelled"

    assert Reservation.objects.filter(event=event, status="pending").count() == 0
    assert Reservation.objects.filter(event=event, status="confirmed").count() == 0
    assert Reservation.objects.filter(event=event, status="rejected").count() == 3

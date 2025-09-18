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
def test_cancel_reservation_twice_second_call_404():

    organizer = CustomUser.objects.create_user(email=unique_email(), password="pass")

    u1 = CustomUser.objects.create_user(email="u1@example.com", password="pass")

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

    client.force_authenticate(user=u1)

    res = Reservation.objects.create(event=event, user=u1, status="confirmed")

    resp1 = client.delete(f"/api/reservations/{res.id}/")

    resp2 = client.delete(f"/api/reservations/{res.id}/")

    assert resp1.status_code == 200

    assert not Reservation.objects.filter(id=res.id).exists()

    assert resp2.status_code == 404

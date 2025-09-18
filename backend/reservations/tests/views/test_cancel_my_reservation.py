from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone
from events.models import Event
from reservations.models import Reservation
from rest_framework.test import APIClient
from users.models import CustomUser


@pytest.mark.django_db
def test_cancel_my_confirmed_reservation_promotes_waitlist_and_broadcasts():

    organizer = CustomUser.objects.create_user(
        email="organizer@example.com", password="pass"
    )

    u1 = CustomUser.objects.create_user(email="u1@example.com", password="pass")
    u2 = CustomUser.objects.create_user(email="u2@example.com", password="pass")

    now = timezone.now()

    event = Event.objects.create(
        title="Test",
        location="Online",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=1, hours=2),
        organizer=organizer,
        status="published",
        seats_limit=1,
    )

    client = APIClient()

    client.force_authenticate(user=u1)

    res = Reservation.objects.create(event=event, user=u1, status="confirmed")

    Reservation.objects.create(event=event, user=u2, status="pending")

    with (
        patch(
            "reservations.views.cancel_my_reservation.promote_from_waitlist_fill"
        ) as promote_mock,
        patch(
            "reservations.views.cancel_my_reservation.broadcast_event_metrics"
        ) as broadcast_mock,
    ):

        resp = client.delete(f"/api/reservations/{res.id}/")

    assert resp.status_code == 200

    assert not Reservation.objects.filter(id=res.id).exists()

    assert promote_mock.call_count == 1
    assert broadcast_mock.call_count == 1


@pytest.mark.django_db
def test_cancel_pending_reservation_does_not_promote_but_broadcasts():

    organizer = CustomUser.objects.create_user(
        email="organizer@example.com", password="pass"
    )

    u1 = CustomUser.objects.create_user(email="u1@example.com", password="pass")

    now = timezone.now()

    event = Event.objects.create(
        title="Test",
        location="Online",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=1, hours=2),
        organizer=organizer,
        status="published",
        seats_limit=1,
    )

    client = APIClient()

    client.force_authenticate(user=u1)

    res = Reservation.objects.create(event=event, user=u1, status="pending")

    with (
        patch(
            "reservations.views.cancel_my_reservation.promote_from_waitlist_fill"
        ) as promote_mock,
        patch(
            "reservations.views.cancel_my_reservation.broadcast_event_metrics"
        ) as broadcast_mock,
    ):

        resp = client.delete(f"/api/reservations/{res.id}/")

    assert promote_mock.call_count == 0
    assert broadcast_mock.call_count == 1

    assert not Reservation.objects.filter(id=res.id).exists()

    assert resp.status_code == 200

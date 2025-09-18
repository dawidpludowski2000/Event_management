from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone
from events.models import Event
from reservations.models import Reservation
from rest_framework.test import APIClient
from users.models import CustomUser


@pytest.mark.django_db
def test_inspect_view_allows_organizer_returns_200():

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

    client.force_authenticate(user=organizer)

    res = Reservation.objects.create(user=u1, event=event, status="confirmed")

    resp = client.get(f"/api/reservations/{res.id}/inspect/")

    assert resp.status_code == 200

    data = resp.json()

    assert data.get("reservation_id") == res.id
    assert data.get("user_email") == u1.email
    assert data.get("event_id") == event.id
    assert data.get("event_title") == event.title


@pytest.mark.django_db
def test_inspect_view_denies_other_user_returns_403():

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

    client.force_authenticate(user=u2)

    res = Reservation.objects.create(event=event, user=u1, status="confirmed")

    resp = client.get(f"/api/reservations/{res.id}/inspect/")

    assert resp.status_code == 403


@pytest.mark.django_db
def test_inspect_view_requires_auth_returns_401():

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

    res = Reservation.objects.create(event=event, user=u1, status="pending")

    resp = client.get(f"/api/reservations/{res.id}/inspect/")

    assert resp.status_code == 401

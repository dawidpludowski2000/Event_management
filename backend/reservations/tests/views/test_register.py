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
def test_register_requires_auth():
    organizer = CustomUser.objects.create_user(email=unique_email(), password="pass")

    now = timezone.now()

    event = Event.objects.create(
        title="Test",
        location="Online",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=1, hours=2),
        seats_limit=10,
        organizer=organizer,
        status="published",
    )

    client = APIClient()

    resp = client.post(f"/api/events/{event.id}/register/")

    assert resp.status_code == 401
    assert Reservation.objects.filter(event=event).count() == 0

    print("JSON:", resp.json())


@pytest.mark.django_db
def test_reservation_endpoint():
    organizer = CustomUser.objects.create_user(email=unique_email(), password="pass")

    u1 = CustomUser.objects.create_user(email="u1@example.com", password="pass")

    now = timezone.now()

    event = Event.objects.create(
        title="Test",
        location="Online",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=1, hours=2),
        seats_limit=10,
        organizer=organizer,
        status="published",
    )

    client = APIClient()

    client.force_authenticate(user=u1)

    resp = client.post(f"/api/events/{event.id}/register/")

    assert resp.status_code == 201

    assert (
        Reservation.objects.filter(user=u1, event=event, status="pending").count() == 1
    )


@pytest.mark.django_db
def test_user_cannot_register_twice():
    organizer = CustomUser.objects.create_user(email=unique_email(), password="pass")
    u1 = CustomUser.objects.create_user(email="u1@example.com", password="pass")

    now = timezone.now()
    event = Event.objects.create(
        title="Test",
        location="Online",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=1, hours=2),
        seats_limit=10,
        organizer=organizer,
        status="published",
    )

    client = APIClient()
    client.force_authenticate(user=u1)

    resp1 = client.post(f"/api/events/{event.id}/register/")
    assert resp1.status_code == 201

    resp2 = client.post(f"/api/events/{event.id}/register/")
    assert resp2.status_code == 400

    data2 = resp2.json()
    
    # najpierw próbujemy główne message
    msg = data2.get("message", "").lower()

    # jak surowy error jest w errors.detail to go bierzemy zamiast generycznego "Validation error"
    errors = data2.get("errors", {})
    if isinstance(errors, dict):
        detail = errors.get("detail") or errors.get("errors", {}).get("detail")
    if isinstance(detail, list):
        detail = detail[0]
    if detail:
        msg = (msg + " " + str(detail)).lower()

    assert "już" in msg or "already" in msg



    assert Reservation.objects.filter(user=u1, event=event).count() == 1


@pytest.mark.django_db
def test_register_rejects_draft_event():
    organizer = CustomUser.objects.create_user(email=unique_email(), password="pass")

    u1 = CustomUser.objects.create_user(email="u1@example.com", password="pass")

    now = timezone.now()

    event = Event.objects.create(
        title="Test",
        location="Online",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=1, hours=2),
        seats_limit=10,
        organizer=organizer,
    )

    client = APIClient()

    client.force_authenticate(user=u1)

    client.post(f"/api/events/{event.id}/register/")

    assert Reservation.objects.filter(user=u1, event=event).count() == 0

import uuid
from datetime import timedelta

import pytest
from django.utils import timezone
from events.models import Event
from reservations.models import Reservation
from rest_framework.test import APIClient
from users.models import CustomUser


@pytest.mark.django_db
def test_qr_ticket_owner_confirmed_returns_png(unique_email):
    organizer = CustomUser.objects.create_user(email=unique_email, password="pass")

    u1 = CustomUser.objects.create_user(
        email=f"user-{uuid.uuid4().hex[:6]}@example.com", password="pass"
    )

    now = timezone.now()

    event = Event.objects.create(
        title="Test",
        location="Online",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=2, hours=2),
        organizer=organizer,
        status="published",
        seats_limit=1,
    )

    client = APIClient()
    client.force_authenticate(user=u1)

    res = Reservation.objects.create(event=event, user=u1, status="confirmed")

    resp = client.get(f"/api/reservations/{res.id}/ticket/")

    assert resp.status_code == 200
    assert resp["Content-Type"] == "image/png"
    assert len(resp.content) > 0


@pytest.mark.django_db
def test_qr_ticket_pending_reservation_returns_404(unique_email):
    organizer = CustomUser.objects.create_user(email=unique_email, password="pass")

    u1 = CustomUser.objects.create_user(
        email=f"user-{uuid.uuid4().hex[:6]}@example.com", password="pass"
    )

    now = timezone.now()

    event = Event.objects.create(
        title="Test",
        location="Online",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=2, hours=2),
        organizer=organizer,
        status="published",
        seats_limit=1,
    )

    client = APIClient()
    client.force_authenticate(user=u1)

    res = Reservation.objects.create(event=event, user=u1, status="pending")

    resp = client.get(f"/api/reservations/{res.id}/ticket/")

    assert resp.status_code == 404
    assert not resp.content


@pytest.mark.django_db
def test_qr_ticket_rejected_reservation_returns_404(unique_email):
    organizer = CustomUser.objects.create_user(email=unique_email, password="pass")

    u1 = CustomUser.objects.create_user(
        email=f"user-{uuid.uuid4().hex[:6]}@example.com", password="pass"
    )

    now = timezone.now()

    event = Event.objects.create(
        title="Test",
        location="Online",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=2, hours=2),
        organizer=organizer,
        status="published",
        seats_limit=1,
    )

    client = APIClient()
    client.force_authenticate(user=u1)

    res = Reservation.objects.create(event=event, user=u1, status="rejected")

    resp = client.get(f"/api/reservations/{res.id}/ticket/")

    assert resp.status_code == 404
    assert not resp.content


@pytest.mark.django_db
def test_qr_ticket_other_user_cannot_access_returns_404(unique_email):
    organizer = CustomUser.objects.create_user(email=unique_email, password="pass")

    u1 = CustomUser.objects.create_user(
        email=f"user-{uuid.uuid4().hex[:6]}@example.com", password="pass"
    )
    u2 = CustomUser.objects.create_user(
        email=f"user-{uuid.uuid4().hex[:6]}@example.com", password="pass"
    )

    now = timezone.now()

    event = Event.objects.create(
        title="Test",
        location="Online",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(days=2, hours=2),
        organizer=organizer,
        status="published",
        seats_limit=1,
    )

    client = APIClient()
    client.force_authenticate(user=u2)

    res = Reservation.objects.create(event=event, user=u1, status="confirmed")

    resp = client.get(f"/api/reservations/{res.id}/ticket/")

    assert resp.status_code == 404
    assert not resp.content

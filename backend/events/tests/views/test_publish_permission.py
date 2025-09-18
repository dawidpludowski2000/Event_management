from datetime import datetime, timedelta

import pytest
from django.utils import timezone
from events.models import Event
from rest_framework.test import APIClient
from tests.utils import unique_email
from users.models import CustomUser


@pytest.mark.django_db
def test_publish_event_forbidden_for_non_organizer_returns_403():

    organizer = CustomUser.objects.create_user(email=unique_email(), password="pass")

    u1 = CustomUser.objects.create_user(email="u1@example.com", password="pass")

    now = timezone.now()

    event = Event.objects.create(
        title="Test",
        location="Online",
        start_time=now + timedelta(days=1),
        end_time=now + timedelta(hours=2),
        seats_limit=2,
        status="draft",
        organizer=organizer,
    )

    client = APIClient()

    client.force_authenticate(user=u1)

    resp = client.post(f"/api/events/organizer/{event.id}/publish/")

    assert resp.status_code == 403
    event.refresh_from_db()

    assert event.status == "draft"

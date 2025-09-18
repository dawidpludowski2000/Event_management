import pytest
from rest_framework.test import APIClient
from events.models import Event
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
def test_create_event_requires_auth_returns_401():
    
    client = APIClient()
    payload = {
        "title": "Unauthorized Event",
        "location": "Nowhere",
        "start_time": (timezone.now() + timedelta(days=1)).isoformat(),
        "end_time": (timezone.now() + timedelta(days=1, hours=2)).isoformat(),
        "seats_limit": 10,
    }

    
    resp = client.post("/api/events/organizer/events/create/", payload, format="json")

    initial = Event.objects.count()
    assert resp.status_code == 401
    assert Event.objects.count() == initial
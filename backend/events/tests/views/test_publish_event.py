import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser
from events.models import Event
from reservations.models import Reservation

from tests.utils import unique_email


@pytest.mark.django_db
def test_publish_event_invalid_dates_returns_400():

    organizer = CustomUser.objects.create_user(email=unique_email(), password="pass")


    now = timezone.now() 
    
    event = Event.objects.create(
        title= "Test",
        location= "Online",
        start_time= now + timedelta(days=1),
        end_time= now + timedelta(hours=2),
        seats_limit= 2,
        status= "draft",
        organizer= organizer
    )


    client= APIClient()

    client.force_authenticate(user=organizer)

    resp = client.post(f"/api/events/organizer/{event.id}/publish/")

    assert resp.status_code == 400
    
    event.refresh_from_db()
    
    assert event.status == "draft"



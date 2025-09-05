import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta

from users.models import CustomUser
from events.models import Event
from reservations.models import Reservation


@pytest.mark.django_db
def test_confirm_blocked_when_full_returns_400_and_no_side_effects():

    organizer = CustomUser.objects.create_user(email="org@example.com", password="pass")

    u1 = CustomUser.objects.create_user(email="u1@example.com", password="pass")
    u2 = CustomUser.objects.create_user(email="u2@example.com", password="pass")
    


    now = timezone.now() 
    
    event = Event.objects.create(
        title= "Test",
        location= "Online",
        start_time= now + timedelta(days=1),
        end_time= now + timedelta(days=2, hours=2),
        seats_limit= 1,
        status= "published",
        organizer= organizer
    )


    Reservation.objects.create(event=event, user=u2, status="confirmed")

    res = Reservation.objects.create(event=event, user=u1, status="pending")
    

    client = APIClient()
    client.force_authenticate(user=organizer)

    with (
        patch("reservations.views.reservation_status_update.broadcast_event_metrics") as broadcast_mock,
        patch("reservations.views.reservation_status_update.send_reservation_status_email") as mail_mock
    ):
        
        resp = client.patch(f"/api/reservations/{res.id}/status/",
                            data={"status": "confirmed"},
                            format="json",
                            )
         
        


    assert resp.status_code == 400
    
    res.refresh_from_db()

    assert res.status == "pending"
    
    assert broadcast_mock.call_count == 0

    assert mail_mock.call_count == 0
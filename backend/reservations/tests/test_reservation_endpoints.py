import pytest
from rest_framework.test import APIClient
from unittest.mock import patch

from django.utils import timezone
from datetime import timedelta

from users.models.user import CustomUser
from events.models import Event
from reservations.models import Reservation
from reservations.services.waitlist_service import promote_from_waitlist_fill


@pytest.mark.django_db
def test_reservation_endpoint():

    organizer = CustomUser.objects.create_user(email="org@example.com", password="pass")

    u1 = CustomUser.objects.create_user(email="u1@example.com", password="pass")

    now = timezone.now()

    event = Event.objects.create(
        title= "Test",
        location= "Online",
        start_time= now + timedelta(days=1),
        end_time= now + timedelta(days=1, hours=2),
        seats_limit= 10,
        organizer= organizer,
        status= "published"
    )


    client = APIClient() 

    client.force_authenticate(user=u1)

    resp = client.post(f"/api/events/{event.id}/register/")

    

    assert resp.status_code == 201


    assert Reservation.objects.filter(user=u1, event=event, status="pending").count() == 1


@pytest.mark.django_db
def test_user_cannot_register_twice():
    
    organizer = CustomUser.objects.create_user(email="org@example.com", password="pass")
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
    assert "już" in data2.get("detail", "").lower() or "already" in data2.get("detail", "").lower()

    assert Reservation.objects.filter(user=u1, event=event).count() == 1


@pytest.mark.django_db
def test_register_requires_auth():

    organizer = CustomUser.objects.create_user(email="org@example.com", password="pass")

    now = timezone.now()

    event = Event.objects.create(
        title= "Test",
        location= "Online",
        start_time= now + timedelta(days=1),
        end_time= now + timedelta(days=1, hours=2),
        seats_limit= 10,
        organizer= organizer,
        status= "published"
    )

    client = APIClient()

    resp = client.post(f"/api/events/{event.id}/register/")

    

    assert resp.status_code == 401
    assert Reservation.objects.filter(event=event).count() == 0
    

    print("JSON:", resp.json())

@pytest.mark.django_db
def test_register_rejects_draft_event():

    organizer = CustomUser.objects.create_user(email="org@example.com", password="pass")

    u1 = CustomUser.objects.create_user(email="u1@example.com", password="pass")

    
    now = timezone.now()

    event = Event.objects.create(
        title= "Test",
        location= "Online",
        start_time= now + timedelta(days=1),
        end_time= now + timedelta(days=1, hours=2),
        seats_limit= 10,
        organizer= organizer,
        
    )

    client = APIClient()

    client.force_authenticate(user=u1)


    resp = client.post(f"/api/events/{event.id}/register/")

    assert Reservation.objects.filter(user=u1, event=event).count() == 0


@pytest.mark.django_db
def test_checkin_requires_confirmed_status():

    organizer = CustomUser.objects.create_user(email="org@example.com", password="pass")

    u1 = CustomUser.objects.create_user(email="u1@example.com", password="pass")

    now = timezone.now()

    event = Event.objects.create(
        title= "Test",
        location= "Online",
        start_time= now + timedelta(days=1),
        end_time= now + timedelta(days=1, hours=2),
        seats_limit= 10,
        organizer= organizer,
        status= "published"
    )


    res = Reservation.objects.create(event=event, user=u1, status="pending")



    client = APIClient()

    client.force_authenticate(user=organizer)

    resp = client.post(f"/api/reservations/{res.id}/check-in/")



    assert resp.status_code == 400
    assert "potwierdzone" in resp.json().get("detail", "").lower()

    res.refresh_from_db()
    assert res.checked_in is False


@pytest.mark.django_db
def test_checkin_confirmed_is_idempotent_and_broadcasts_once():

    organizer = CustomUser.objects.create_user(email="org@example.com", password="pass")

    u1 = CustomUser.objects.create_user(email="u1@example.com", password="pass")

    now = timezone.now()

    event = Event.objects.create(
        title= "Test",
        location= "Online",
        start_time= now + timedelta(days=1),
        end_time= now + timedelta(days=1, hours=2),
        seats_limit= 10,
        organizer= organizer,
        status= "published"
    )

    client = APIClient()

    client.force_authenticate(user=organizer)

    res = Reservation.objects.create(event=event, user=u1, status="confirmed")

    with patch("reservations.views.organizer_reservation_check_in_ticket.broadcast_event_metrics") as broadcast_mock:
        resp1 = client.post(f"/api/reservations/{res.id}/check-in/")
        resp2 = client.post(f"/api/reservations/{res.id}/check-in/")

    assert broadcast_mock.call_count == 1

    assert resp1.status_code == 200 

    data1 = resp1.json()
    assert data1.get("checked_in") is True
    assert data1.get("reservation_id") == res.id

    res.refresh_from_db()
    assert res.checked_in is True

    assert resp2.status_code == 200
    data2 = resp2.json()
    assert "oznaczona" in data2.get("detail", "").lower() or "already" in data2.get("detail", "").lower()

    res.refresh_from_db()
    assert res.checked_in is True


@pytest.mark.django_db
def test_checkin_forbidden_for_non_organizer():

    organizer = CustomUser.objects.create_user(email= "org@example.com", password= "pass")

    u1 = CustomUser.objects.create_user(email="u1@example.com", password="pass")


    now = timezone.now()

    event = Event.objects.create(
        title= "Test",
        location= "Online",
        start_time= now + timedelta(days=1),
        end_time= now + timedelta(days=1, hours=2),
        seats_limit= 10,
        organizer= organizer,
        status= "published"
    )

    res = Reservation.objects.create(event=event, user=u1, status="confirmed")

    client = APIClient()

    client.force_authenticate(user=u1)

    resp = client.post(f"/api/reservations/{res.id}/check-in/")

    assert resp.status_code == 403

    res.refresh_from_db()

    

    assert res.checked_in is False 



@pytest.mark.django_db
def test_cancel_my_confirmed_reservation_promotes_waitlist_and_broadcasts():

    organizer = CustomUser.objects.create(email="organizer@example.com", password="pass")

    u1 = CustomUser.objects.create(email="u1@example.com", password="pass")
    u2 = CustomUser.objects.create(email="u2@example.com", password="pass")

    now = timezone.now()

    event = Event.objects.create(
        title= "Test",
        location= "Online",
        start_time= now + timedelta(days=1),
        end_time= now + timedelta(days=1, hours=2),
        organizer= organizer,
        status= "published",
        seats_limit= 1
    )


    client = APIClient()

    client.force_authenticate(user=u1)

    res = Reservation.objects.create(event=event, user=u1, status="confirmed")
    
    Reservation.objects.create(event=event, user=u2, status="pending")


    with ( 
        patch("reservations.views.cancel_my_reservation.promote_from_waitlist_fill") as promote_mock,
        patch("reservations.views.cancel_my_reservation.broadcast_event_metrics") as broadcast_mock
        ):

        resp = client.delete(f"/api/reservations/{res.id}/")

        
    assert resp.status_code == 200

    assert not Reservation.objects.filter(id=res.id).exists()

    assert promote_mock.call_count == 1
    assert broadcast_mock.call_count == 1




    
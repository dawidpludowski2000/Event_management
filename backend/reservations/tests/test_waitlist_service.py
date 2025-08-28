import pytest

from datetime import timedelta
from unittest.mock import patch
from django.utils import timezone


from users.models.managers import CustomUserManager
from users.models.user import CustomUser
from events.models import Event
from reservations.models import Reservation

from reservations.services.waitlist_service import promote_from_waitlist_fill

@pytest.mark.django_db
def test_promote_from_waitlist_happy_path():

    organizer = CustomUser.objects.create_user(email="org@example.com", password="pass")

    u1 = CustomUser.objects.create_user(email="u1@example.com", password="pass")
    u2 = CustomUser.objects.create_user(email="u2@example.com", password="pass")
    u3 = CustomUser.objects.create_user(email="u3@example.com", password="pass")

    now = timezone.now()

    event = Event.objects.create(
        title= "Test Event",
        location= "Online",
        start_time= now + timedelta(days=1),
        end_time= now + timedelta(days=1, hours=2),
        seats_limit= 3,
        organizer= organizer
    )

    u4 = CustomUser.objects.create_user(email="u4@example.com", password="pass")

    Reservation.objects.create(user=u1, event=event, status="confirmed")

    now = timezone.now()
    Reservation.objects.create(user=u2, event=event, status="pending", created_at=now - timedelta(minutes=30))  # najstarszy
    Reservation.objects.create(user=u3, event=event, status="pending", created_at=now - timedelta(minutes=20))
    Reservation.objects.create(user=u4, event=event, status="pending", created_at=now - timedelta(minutes=10))  # najmłodszy


    assert Reservation.objects.filter(event=event, status="confirmed").count() == 1
    assert Reservation.objects.filter(event=event, status="pending").count() == 3


    with patch("reservations.services.waitlist_service.send_reservation_status_email") as mail_mock:
        promoted = promote_from_waitlist_fill(event)

    expected_slots = event.seats_limit - 1

    assert isinstance(promoted, list)
    assert len(promoted) == expected_slots


    confirmed_after = Reservation.objects.filter(event=event, status="confirmed").count()
    assert confirmed_after == 1 + expected_slots

    promoted_ids = {r.id for r in promoted}
    assert Reservation.objects.filter(id__in=promoted_ids, status="confirmed").count() == expected_slots

   
    assert mail_mock.call_count == expected_slots



@pytest.mark.django_db
def test_promote_from_waitlist_no_free_slots():

    organizer = CustomUser.objects.create_user(email="organizer@example.com", password="pass")

    now = timezone.now()

    event = Event.objects.create(
        title= "Test Slots",
        location= "Loc",
        start_time= now + timedelta(days=1),
        end_time= now + timedelta(days=1, hours=2),
        seats_limit= 2,
        organizer= organizer
    )


    u1 = CustomUser.objects.create_user(email="u1@example.com", password="pass")
    u2 = CustomUser.objects.create_user(email="u2@example.com", password="pass")

    u3 = CustomUser.objects.create_user(email="u3@example.com", password="pass")
    u4 = CustomUser.objects.create_user(email="u4@example.com", password="pass")
    u5 = CustomUser.objects.create_user(email="u5@example.com", password="pass")


    Reservation.objects.create(user=u1, event=event, status="confirmed")
    Reservation.objects.create(user=u2, event=event, status="confirmed")

    Reservation.objects.create(user=u3, event=event, status="pending")
    Reservation.objects.create(user=u4, event=event, status="pending")
    Reservation.objects.create(user=u5, event=event, status="pending")


    assert Reservation.objects.filter(event=event, status="confirmed").count() == 2

    assert Reservation.objects.filter(event=event, status="pending").count() == 3

    

    with patch("reservations.services.waitlist_service.send_reservation_status_email") as mail_mock:
        promoted = promote_from_waitlist_fill(event)

    # oczekujemy, że nic nie zostanie zpromowane (brak wolnych miejsc)
    assert promoted == [] or len(promoted) == 0

    # potwierdzone nadal 2
    assert Reservation.objects.filter(event=event, status="confirmed").count() == 2

    # i mailer nie został wywołany
    assert mail_mock.call_count == 0
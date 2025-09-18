# backend/reservations/services/waitlist_service.py
from django.db import transaction, connection
from reservations.models import Reservation
from notifications.services.email import send_reservation_status_email
import logging


def promote_from_waitlist_fill(event):
    """
    Promuje tylu oczekujących (status='pending'), ile jest wolnych miejsc w evencie.
    Zwraca listę zpromowanych rezerwacji (obiekty Reservation).
    Działa na SQLite i PostgreSQL (na PG używa SKIP LOCKED).
    """
    # Te zmienne wyjdą z transakcji – wykorzystamy je do wysyłki maili
    to_promote = []

    with transaction.atomic():
        # Odśwież i zablokuj rekord Event (na PG faktycznie zablokuje wiersz)
        event = type(event).objects.select_for_update().get(pk=event.pk)

        # Brak limitu = brak kolejki
        if not event.seats_limit:
            return []

        # Ile jest potwierdzonych
        confirmed_count = Reservation.objects.filter(
            event=event, status="confirmed"
        ).count()

        slots = event.seats_limit - confirmed_count
        if slots <= 0:
            return []

        # Pobierz pierwszych N pending w kolejce
        if connection.vendor == "postgresql":
            # Bezpiecznie przy wielu równoległych procesach
            pending_qs = (
                Reservation.objects
                .select_for_update(skip_locked=True)
                .filter(event=event, status="pending")
                .order_by("created_at")
            )[:slots]
        else:
            # Fallback dla SQLite i innych
            pending_qs = (
                Reservation.objects
                .filter(event=event, status="pending")
                .order_by("created_at")
            )[:slots]

        to_promote = list(pending_qs)
        if not to_promote:
            return []

        # Masowa aktualizacja (szybka i atomowa)
        Reservation.objects.filter(
            pk__in=[r.pk for r in to_promote]
        ).update(status="confirmed")

    # --- Po wyjściu z transakcji: wyślij maile (żeby nie wysłać, jeśli rollback) ---
    for r in to_promote:
        try:
            send_reservation_status_email(
                user_email=r.user.email,
                user_name=r.user.get_username() or r.user.username,
                event_title=r.event.title,
                event_date=r.event.start_time,   # start
                status="confirmed",
                reply_to=r.event.organizer.email,
                event_end=r.event.end_time,      # ładny .ics (koniec)
                event_location=r.event.location, # ładny .ics (lokalizacja)
            )
        except Exception as e:
            # Nie blokuj całego procesu kolejki, jeśli mail padnie

            logger = logging.getLogger(__name__)

            logger.warning("[WAITLIST][MAIL] %s", e)


    return to_promote

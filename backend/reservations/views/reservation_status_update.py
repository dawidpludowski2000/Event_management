from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from events.services.organizer_permissions import IsEventOrganizer
from reservations.models import Reservation
from reservations.serializers.reservation_status_update import ReservationStatusUpdateSerializer
from notifications.services.email import send_reservation_status_email
from events.services.realtime_metrics import broadcast_event_metrics
from config.core.api_response import success, error


class ReservationStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsEventOrganizer]

    def patch(self, request, reservation_id: int):
        try:
            reservation = Reservation.objects.select_related("event", "user").get(id=reservation_id)
        except Reservation.DoesNotExist:
            return error("Rezerwacja nie istnieje.", status=404)

        # Jeśli już potwierdzona lub odrzucona → blokuj
        if reservation.status in ["confirmed", "rejected"]:
            return error("Nie można zmienić statusu zakończonego zgłoszenia.", status=400)

        serializer = ReservationStatusUpdateSerializer(
            instance=reservation, data=request.data, partial=True
        )

        if not serializer.is_valid():
            return error("Błąd walidacji.", errors=serializer.errors, status=400)

        new_status = serializer.validated_data.get("status")

        # Blokada potwierdzenia przy pełnym evencie
        if new_status == "confirmed":
            confirmed_count = Reservation.objects.filter(
                event=reservation.event, status="confirmed"
            ).count()
            if confirmed_count >= reservation.event.seats_limit:
                return error("Brak wolnych miejsc – limit osiągnięty.", status=400)

        # Zapis atomowy
        with transaction.atomic():
            serializer.save()

        # Jeśli rejected → żadnych maili ani broadcastów
        if new_status == "rejected":
            return success("Rezerwacja odrzucona.", {"status": "rejected"})

        # Jeśli confirmed → mail + aktualizacja live
        send_reservation_status_email(
            user_email=reservation.user.email,
            user_name=reservation.user.get_username() or reservation.user.username,
            event_title=reservation.event.title,
            event_date=reservation.event.start_time,
            status=new_status,
            reply_to=reservation.event.organizer.email,
            event_end=reservation.event.end_time,
            event_location=reservation.event.location,
        )

        broadcast_event_metrics(reservation.event)

        return success(
            f"Status rezerwacji zmieniony na '{new_status}'.",
            {"status": new_status}
        )

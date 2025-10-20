from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from events.services.organizer_permissions import IsEventOrganizer
from reservations.models import Reservation
from reservations.serializers.reservation_status_update import ReservationStatusUpdateSerializer
from notifications.services.email import send_reservation_status_email
from events.services.realtime_metrics import broadcast_event_metrics
from common.exceptions import raise_validation
from config.core.api_response import success


class ReservationStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsEventOrganizer]

    def patch(self, request, reservation_id: int):
        try:
            reservation = Reservation.objects.select_related("event").get(id=reservation_id)
        except Reservation.DoesNotExist:
            raise_validation("Rezerwacja nie istnieje.", status=404)

        # Nie można zmieniać statusu zakończonych rezerwacji
        if reservation.status in ["confirmed", "rejected"]:
            raise_validation("Nie można zmienić statusu zakończonego zgłoszenia.", status=400)

        serializer = ReservationStatusUpdateSerializer(
            instance=reservation, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data.get("status")

        # Limit tylko przy potwierdzeniu
        if new_status == "confirmed":
            confirmed_count = Reservation.objects.filter(
                event=reservation.event, status="confirmed"
            ).count()

            if confirmed_count >= reservation.event.seats_limit:
                raise_validation("Brak wolnych miejsc – limit osiągnięty.", status=400)

        # Zapis atomowy
        with transaction.atomic():
            serializer.save()

        # Wyślij email
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

        # Live update broadcast
        broadcast_event_metrics(reservation.event)

        return success(
            f"Status rezerwacji zmieniony na '{new_status}'.",
            {"status": new_status}
        )

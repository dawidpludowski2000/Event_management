import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from events.services.organizer_permissions import IsEventOrganizer
from reservations.models import Reservation
from events.services.realtime_metrics import broadcast_event_metrics
from common.exceptions import raise_validation
from config.core.api_response import success


class OrganizerReservationCheckInView(APIView):
    permission_classes = [IsAuthenticated, IsEventOrganizer]

    def post(self, request, reservation_id: int):
        try:
            reservation = Reservation.objects.select_related("event", "user").get(id=reservation_id)
        except Reservation.DoesNotExist:
            raise_validation("Rezerwacja nie istnieje.", status=404)

        # Rezerwacja musi być potwierdzona
        if reservation.status != "confirmed":
            raise_validation("Check-in możliwy tylko dla potwierdzonych rezerwacji.", status=400)

        # Idempotencja – ponowny check-in nie powoduje błędu
        if reservation.checked_in:
            return success(
                "Rezerwacja była już wcześniej oznaczona jako obecna.",
                {"reservation_id": reservation.id, "checked_in": True}
            )

        reservation.checked_in = True
        reservation.save(update_fields=["checked_in"])

        broadcast_event_metrics(reservation.event)
        logging.getLogger(__name__).info("Check-in confirmed for reservation %s", reservation.id)

        return success(
            "Check-in wykonany.",
            {"reservation_id": reservation.id, "checked_in": True}
        )

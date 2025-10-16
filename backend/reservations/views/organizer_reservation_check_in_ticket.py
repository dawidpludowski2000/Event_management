import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from reservations.models import Reservation
from events.services.organizer_permissions import IsEventOrganizer
from events.services.realtime_metrics import broadcast_event_metrics
from common.exceptions import raise_validation  # ✅ NOWE


class OrganizerReservationCheckInView(APIView):
    permission_classes = [IsAuthenticated, IsEventOrganizer]

    def post(self, request, reservation_id: int):
        try:
            reservation = Reservation.objects.select_related("event", "user").get(id=reservation_id)
        except Reservation.DoesNotExist:
            raise_validation("Rezerwacja nie istnieje.")

        # Nie można zrobić check-in jeśli nie potwierdzono rezerwacji
        if reservation.status != "confirmed":
            raise_validation("Nie można wykonać check-in dla niepotwierdzonej rezerwacji.")

        # Jeśli już jest check-in – endpoint idempotentny
        if reservation.checked_in:
            return Response({
                "success": True,
                "message": "Rezerwacja była już wcześniej oznaczona jako obecna.",
                "data": {
                    "reservation_id": reservation.id,
                    "checked_in": True
                }
            }, status=status.HTTP_200_OK)

        # ✅ Właściwy check-in
        reservation.checked_in = True
        reservation.save(update_fields=["checked_in"])

        # broadcast live metrics update
        broadcast_event_metrics(reservation.event)

        logging.getLogger(__name__).info(
            "Check-in confirmed for reservation %s", reservation.id
        )

        return Response({
            "success": True,
            "message": "Check-in wykonany.",
            "data": {
                "reservation_id": reservation.id,
                "checked_in": True
            }
        }, status=status.HTTP_200_OK)

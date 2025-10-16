import logging

from events.services.organizer_permissions import IsEventOrganizer
from events.services.realtime_metrics import broadcast_event_metrics
from reservations.models import Reservation
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class OrganizerReservationCheckInView(APIView):
    permission_classes = [IsAuthenticated, IsEventOrganizer]

    def post(self, request, reservation_id: int):
        try:
            reservation = Reservation.objects.select_related("event").get(id=reservation_id)
        except Reservation.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Rezerwacja nie istnieje.",
                    "detail": "Rezerwacja nie istnieje."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Check-in tylko dla potwierdzonych
        if reservation.status != "confirmed":
            return Response(
                {
                    "success": False,
                    "message": "Nie można wykonać check-in.",
                    "detail": "Tylko potwierdzone rezerwacje można oznaczyć jako obecne."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Idempotentne — już była oznaczona
        if reservation.checked_in:
            return Response(
                {
                "success": True,
                "message": "Rezerwacja już wcześniej była oznaczona jako obecna.",
                "detail": "Rezerwacja już wcześniej była oznaczona jako obecna.",
                "checked_in": True,
                "reservation_id": reservation.id,
            },
            status=status.HTTP_200_OK
)

        # Normalny check-in
        reservation.checked_in = True
        reservation.save(update_fields=["checked_in"])

        logger = logging.getLogger(__name__)
        logger.info("Check-in OK; broadcasting metrics for event %s", reservation.event.id)

        broadcast_event_metrics(reservation.event)

        return Response(
            {
                "success": True,
                "message": "Check-in wykonany.",
                "checked_in": True,
                "reservation_id": reservation.id,
            },
            status=status.HTTP_200_OK
        )

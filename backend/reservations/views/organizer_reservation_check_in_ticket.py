import logging

from events.services.organizer_permissions import IsEventOrganizer
from events.services.realtime_metrics import broadcast_event_metrics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from reservations.models import Reservation


class OrganizerReservationCheckInView(APIView):
    permission_classes = [IsAuthenticated, IsEventOrganizer]

    def post(self, request, reservation_id: int):

        try:
            reservation = Reservation.objects.select_related("event").get(
                id=reservation_id
            )
        except Reservation.DoesNotExist:

            return Response(
                {"detail": "Rezerwacja nie istnieje."}, status=status.HTTP_404_NOT_FOUND
            )

        # check-in tylko dla potwierdzonych
        if reservation.status != "confirmed":

            return Response(
                {"detail": "Tylko potwierdzone rezerwacje można oznaczyć jako obecne."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if reservation.checked_in:

            return Response(
                {
                    "detail": "Ta rezerwacja jest już oznaczona jako obecna.",
                    "checked_in": True,
                    "reservation_id": reservation.id,
                },
                status=status.HTTP_200_OK,
            )

        reservation.checked_in = True
        reservation.save(update_fields=["checked_in"])

        logger = logging.getLogger(__name__)

        logger.info(
            "Check-in OK; broadcasting metrics for event %s", reservation.event.id
        )

        broadcast_event_metrics(reservation.event)

        return Response(
            {
                "detail": "Check-in wykonany.",
                "checked_in": True,
                "reservation_id": reservation.id,
            },
            status=200,
        )

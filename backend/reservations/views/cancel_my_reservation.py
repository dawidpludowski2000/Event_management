from django.core.exceptions import PermissionDenied
from events.services.realtime_metrics import broadcast_event_metrics
from reservations.models.reservation import Reservation
from reservations.services.waitlist_service import promote_from_waitlist_fill
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class CancelMyReservation(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id)

        except Reservation.DoesNotExist:
            return Response(
                {"detail": "Rezerwacja nie istnieje."}, status=status.HTTP_404_NOT_FOUND
            )

        if reservation.user != request.user:
            raise PermissionDenied("Nie masz uprawnień do anulowania tej rezerwacji.")

        was_confirmed = reservation.status == "confirmed"
        event = reservation.event

        reservation.delete()

        if was_confirmed:
            promote_from_waitlist_fill(event)

        broadcast_event_metrics(event)

        return Response(
            {"detail": "Rezerwacja została anulowana."}, status=status.HTTP_200_OK
        )

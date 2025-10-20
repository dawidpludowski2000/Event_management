from rest_framework import permissions, status
from rest_framework.views import APIView
from reservations.models import Reservation
from config.core.api_response import success, error
from events.services.realtime_metrics import broadcast_event_metrics
from reservations.services.waitlist_service import promote_from_waitlist_fill


class CancelMyReservationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, reservation_id):
        try:
            reservation = Reservation.objects.select_related("event").get(
                id=reservation_id, user=request.user
            )
        except Reservation.DoesNotExist:
            return error("Nie znaleziono rezerwacji.", status=404)

        event = reservation.event
        was_confirmed = reservation.status == "confirmed"

        reservation.delete()

        if was_confirmed:
            promote_from_waitlist_fill(event)

        broadcast_event_metrics(event)

        return success(
            message="Rezerwacja została anulowana.",
            data={"reservation_id": reservation_id},
            status=200
        )

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from config.core.api_response import success, error
from reservations.models import Reservation
from events.services.realtime_metrics import broadcast_event_metrics
from reservations.services.waitlist_service import promote_from_waitlist_fill


class CancelMyReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, reservation_id):
        # Użytkownik może usunąć tylko swoją rezerwację
        try:
            reservation = Reservation.objects.select_related("event").get(
                id=reservation_id, user=request.user
            )
        except Reservation.DoesNotExist:
            return error(message="Reservation not found.", status=404)

        event = reservation.event
        was_confirmed = reservation.status == "confirmed"

        # Usuń rezerwację
        reservation.delete()

        # Jeśli było confirmed, można promować z kolejki
        if was_confirmed:
            promote_from_waitlist_fill(event)

        # Broadcast zawsze, nawet pending -> NULL
        broadcast_event_metrics(event)

        return success(
            message="Reservation cancelled.",
            data={"reservation_id": reservation_id},
            status=200,
        )

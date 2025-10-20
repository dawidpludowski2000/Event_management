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
            return error("Nie masz takiej rezerwacji lub już została anulowana.", status=404)

        if reservation.status == "cancelled":
            return success(
                "Rezerwacja została już anulowana.",
                data={"reservation_id": reservation.id},
                status=200
            )

        was_confirmed = reservation.status == "confirmed"

        reservation.status = "cancelled"
        reservation.save(update_fields=["status"])

        if was_confirmed:
            promote_from_waitlist_fill(reservation.event)

        broadcast_event_metrics(reservation.event)

        return success(
            message="Rezerwacja została anulowana.",
            data={"reservation_id": reservation.id},
            status=status.HTTP_200_OK
        )

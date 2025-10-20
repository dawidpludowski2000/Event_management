from events.models import Event
from reservations.models import Reservation
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from config.core.api_response import success, error


class MySingleReservationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return error("Event not found.", status=404)

        reservation = Reservation.objects.filter(event=event, user=request.user).first()

        current_confirmed = Reservation.objects.filter(
            event=event, status="confirmed"
        ).count()

        max_count = event.seats_limit or None
        free_slots = (max_count - current_confirmed) if max_count is not None else None
        is_full = max_count is not None and current_confirmed >= max_count

        data = {
            "status": reservation.status if reservation else "NONE",
            "full": False if reservation else is_full,
            "free_slots": free_slots,
            "max_participants": max_count,
        }

        return success("Reservation status fetched.", data)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from reservations.models import Reservation
from events.models import Event
from config.core.api_response import success, error


class MySingleReservationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        # Event musi istnieć
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return error(message="Event not found.", status=404)

        # Czy user ma rezerwację?
        reservation = Reservation.objects.filter(event=event, user=request.user).first()

        # Oblicz parametry
        confirmed_count = Reservation.objects.filter(
            event=event, status="confirmed"
        ).count()

        max_participants = event.seats_limit or None
        free_slots = (
            max_participants - confirmed_count if max_participants is not None else None
        )
        is_full = max_participants is not None and confirmed_count >= max_participants

        return success(
            message="Reservation status fetched.",
            data={
                "status": reservation.status if reservation else "NONE",
                "full": False if reservation else is_full,
                "free_slots": free_slots,
                "max_participants": max_participants,
            },
            status=200,
        )

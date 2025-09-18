from events.models import Event
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from reservations.models import Reservation


class MySingleReservationDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):

        try:
            event = Event.objects.get(id=event_id)

        except Event.DoesNotExist:

            return Response(
                {"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND
            )

        reservation = Reservation.objects.filter(event=event, user=request.user).first()

        current_confirmed = Reservation.objects.filter(
            event=event, status="confirmed"
        ).count()

        max_count = event.seats_limit or None
        free_slots = (max_count - current_confirmed) if max_count else None

        is_full = max_count is not None and current_confirmed >= max_count

        if reservation:
            return Response(
                {
                    "status": reservation.status,
                    "full": False,  # bo jesteś już zapisany
                    "free_slots": free_slots,
                    "max_participants": max_count,
                },
                status=200,
            )

        return Response(
            {
                "status": "NONE",
                "full": is_full,
                "free_slots": free_slots,
                "max_participants": max_count,
            },
            status=200,
        )

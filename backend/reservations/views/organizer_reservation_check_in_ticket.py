from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import status

from config.core.api_response import success, error
from reservations.models import Reservation
from events.services.organizer_permissions import IsEventOrganizer
from events.services.realtime_metrics import broadcast_event_metrics


class OrganizerReservationCheckInView(APIView):
    permission_classes = [IsAuthenticated, IsEventOrganizer]

    def post(self, request, reservation_id: int):
        try:
            reservation = Reservation.objects.select_related("event", "user").get(id=reservation_id)
        except Reservation.DoesNotExist:
            raise NotFound("Rezerwacja nie istnieje.")

        # check-in tylko dla confirmed
        if reservation.status != "confirmed":
            return error(
                message="Check-in jest możliwy tylko dla rezerwacji potwierdzone.",
                errors={"detail": "Rezerwacja nie ma statusu confirmed."},
                status=400,
            )

        # idempotencja – jeśli już było check-in
        if reservation.checked_in:
            return success(
                message="Rezerwacja była już wcześniej oznaczona jako obecna.",
                data={
                    "reservation_id": reservation.id,
                    "checked_in": True,
                    "detail": "Rezerwacja już wcześniej była oznaczona jako obecna.",
                },
                status=status.HTTP_200_OK,
            )

        # wykonaj check-in po raz pierwszy
        reservation.checked_in = True
        reservation.save(update_fields=["checked_in"])

        # broadcast tylko przy pierwszym check-in
        broadcast_event_metrics(reservation.event)

        return success(
            message="Check-in wykonany pomyślnie.",
            data={
                "reservation_id": reservation.id,
                "checked_in": True,
                "detail": "Check-in wykonany pomyślnie.",
            },
            status=status.HTTP_200_OK,
        )

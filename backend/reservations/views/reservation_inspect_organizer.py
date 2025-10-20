from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from events.services.organizer_permissions import IsEventOrganizer
from reservations.models import Reservation
from reservations.serializers.reservation_inspect import ReservationInspectSerializer
from config.core.api_response import success, error


class OrganizerReservationInspectView(APIView):
    permission_classes = [IsAuthenticated, IsEventOrganizer]

    def get(self, request, reservation_id: int):
        try:
            reservation = Reservation.objects.select_related("user", "event").get(id=reservation_id)
        except Reservation.DoesNotExist:
            return error(message="Reservation not found.", status=404)

        data = ReservationInspectSerializer(reservation).data
        return success(
            message="Reservation details retrieved.",
            data=data,
            status=200
        )

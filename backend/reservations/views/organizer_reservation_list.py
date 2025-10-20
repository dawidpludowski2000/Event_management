from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from reservations.models import Reservation
from reservations.serializers.organizer_reservation_list import OrganizerReservationListSerializer
from config.core.api_response import success


class OrganizerReservationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reservations = (
            Reservation.objects
            .filter(event__organizer=request.user)
            .select_related("event", "user")
            .order_by("-created_at")
        )
        data = OrganizerReservationListSerializer(reservations, many=True).data
        return success(
            message="Organizer reservation list retrieved.",
            data=data,
            status=200
        )

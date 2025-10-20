from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from reservations.models import Reservation
from reservations.serializers.organizer_reservation_list import (
    OrganizerReservationListSerializer,
)
from events.services.organizer_permissions import IsEventOrganizer
from config.core.api_response import success


class OrganizerReservationView(APIView):
    permission_classes = [IsAuthenticated, IsEventOrganizer]

    def get(self, request):
        reservations = (
            Reservation.objects.filter(event__organizer=request.user)
            .select_related("event", "user")
            .order_by("-created_at")
        )
        data = OrganizerReservationListSerializer(reservations, many=True).data
        return success("Lista rezerwacji organizatora pobrana.", data)

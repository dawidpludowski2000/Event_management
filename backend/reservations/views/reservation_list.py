from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from events.models.event import Event
from events.services.organizer_permissions import IsEventOrganizer
from reservations.models import Reservation
from reservations.serializers.reservation_list import ReservationListSerializer
from config.core.api_response import success, error


class ParticipantsListView(APIView):
    permission_classes = [IsAuthenticated, IsEventOrganizer]

    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return error(message="Event not found.", status=404)

        reservations = (
            Reservation.objects
            .filter(event=event)
            .select_related("user")
            .order_by("-created_at")
        )

        data = ReservationListSerializer(reservations, many=True).data
        return success(
            message="Participants list retrieved.",
            data=data,
            status=200
        )

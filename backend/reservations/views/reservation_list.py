from events.models.event import Event
from events.services.organizer_permissions import IsEventOrganizer
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from reservations.models import Reservation
from reservations.serializers.reservation_list import ReservationListSerializer


class ParticipantsListView(generics.ListAPIView):

    serializer_class = ReservationListSerializer
    permission_classes = [IsAuthenticated, IsEventOrganizer]

    def get_queryset(self):

        event_id = self.kwargs["event_id"]

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise PermissionDenied("Wydarzenie nie istnieje.")

        return Reservation.objects.filter(event=event)

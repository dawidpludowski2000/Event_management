from rest_framework import generics, permissions

from reservations.models.reservation import Reservation
from reservations.serializers.organizer_reservation_list import (
    OrganizerReservationListSerializer,
)


class OrganizerReservationView(generics.ListAPIView):

    serializer_class = OrganizerReservationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(
            event__organizer=self.request.user
        ).select_related("event", "user")

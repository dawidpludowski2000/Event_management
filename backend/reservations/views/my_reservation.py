from reservations.models import Reservation
from reservations.serializers.reservation_list import ReservationListSerializer
from rest_framework import generics, permissions


class MyReservationsView(generics.ListAPIView):
    serializer_class = ReservationListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).select_related(
            "event"
        )

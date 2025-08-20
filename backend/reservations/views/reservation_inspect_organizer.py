from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from reservations.models import Reservation
from reservations.serializers.reservation_inspect import ReservationInspectSerializer
from events.services.organizer_permissions import IsEventOrganizer

class OrganizerReservationInspectView(APIView):
    permission_classes = [IsAuthenticated, IsEventOrganizer]  # sprawdza po reservation_id

    def get(self, request, reservation_id: int):
        try:
            reservation = Reservation.objects.select_related("user", "event").get(id=reservation_id)
        except Reservation.DoesNotExist:
            return Response({"detail": "Rezerwacja nie istnieje."}, status=status.HTTP_404_NOT_FOUND)

        # IsEventOrganizer wpuści tylko organizatora tego eventu (po reservation_id)
        data = ReservationInspectSerializer(reservation).data
        return Response(data, status=200)

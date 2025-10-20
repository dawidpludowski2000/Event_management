from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from reservations.models import Reservation
from reservations.serializers.reservation_list import ReservationListSerializer
from config.core.api_response import success

class MyReservationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reservations = Reservation.objects.filter(user=request.user).select_related("event")
        serializer = ReservationListSerializer(reservations, many=True)
        return success(
            message="Lista rezerwacji pobrana",
            data=serializer.data,
            status=200
        )

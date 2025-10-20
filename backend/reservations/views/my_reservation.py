from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from reservations.models import Reservation
from reservations.serializers.reservation_list import ReservationListSerializer
from config.core.api_response import success


class MyReservationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Reservation.objects.filter(user=request.user).select_related("event")
        ser = ReservationListSerializer(queryset, many=True)
        return success("Lista rezerwacji pobrana pomyślnie.", ser.data)

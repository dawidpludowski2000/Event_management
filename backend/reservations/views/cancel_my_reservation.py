from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from reservations.models import Reservation
from common.exceptions import raise_validation


class CancelMyReservationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id, user=request.user)
        except Reservation.DoesNotExist:
            raise_validation("Nie masz takiej rezerwacji lub już została anulowana.")

        if reservation.status == "cancelled":
            raise_validation("Rezerwacja została już anulowana.")

        reservation.status = "cancelled"
        reservation.save(update_fields=["status"])

        return Response(
            {
                "success": True,
                "message": "Rezerwacja została anulowana.",
                "data": {"reservation_id": reservation_id},
            },
            status=status.HTTP_200_OK,
        )

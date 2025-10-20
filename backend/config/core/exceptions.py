import io
import qrcode
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from reservations.models import Reservation

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

class ReservationTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, reservation_id: int):
        #  znajdź tylko jeśli rezerwacja należy do użytkownika
        try:
            reservation = Reservation.objects.select_related("event").get(
                id=reservation_id, user=request.user
            )
        except Reservation.DoesNotExist:
            # WYMAGANIE TESTÓW: 404 bez contentu
            return HttpResponse(status=404)

        # bilet tylko dla potwierdzonych — w przeciwnym razie 404 (bez treści)
        if reservation.status != "confirmed":
            return HttpResponse(status=404)

        # treść QR
        qr_data = f"Reservation:{reservation.id}|Event:{reservation.event.title}"
        qr_img = qrcode.make(qr_data)

        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        buf.seek(0)

        # Zwracamy jako plik PNG
        response = HttpResponse(buf.getvalue(), content_type="image/png")
        response["Content-Disposition"] = f'inline; filename="ticket-{reservation.id}.png"'
        return response


logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return Response(
            {
                "status": "error",
                "error": response.data,
            },
            status=response.status_code,
        )

        
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return Response(
        {
            "status": "error",
            "error": "Internal server error",
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
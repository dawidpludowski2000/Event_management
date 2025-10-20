import io
import logging
import qrcode
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from reservations.models import Reservation

logger = logging.getLogger(__name__)


class ReservationTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, reservation_id: int):
        """
        Zwraca wygenerowany bilet QR jako PNG tylko dla potwierdzonych rezerwacji.
        RESTowo poprawne: jeśli zasób nie istnieje, zwracamy 404 bez JSON-a.
        """
        # Znajdź rezerwację użytkownika
        try:
            reservation = Reservation.objects.select_related("event").get(
                id=reservation_id, user=request.user
            )
        except Reservation.DoesNotExist:
            logger.warning(f"[QR Ticket] Brak rezerwacji ID={reservation_id} dla usera {request.user.id}")
            return HttpResponse(status=404)

        # Dostęp tylko dla potwierdzonych
        if reservation.status != "confirmed":
            logger.info(f"[QR Ticket] Próba dostępu do biletu bez potwierdzenia (res={reservation.id})")
            return HttpResponse(status=404)

        # Generujemy QR code ticket
        qr_data = f"Reservation:{reservation.id}|Event:{reservation.event.title}"
        qr_img = qrcode.make(qr_data)
        buffer = io.BytesIO()
        qr_img.save(buffer, format="PNG")
        buffer.seek(0)

        response = HttpResponse(buffer.getvalue(), content_type="image/png")
        response["Content-Disposition"] = f'inline; filename="ticket-{reservation.id}.png"'
        return response

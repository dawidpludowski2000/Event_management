import io
import qrcode
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from reservations.models import Reservation


class ReservationTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, reservation_id: int):
        # Znajdź rezerwację użytkownika
        try:
            reservation = Reservation.objects.select_related("event").get(
                id=reservation_id, user=request.user
            )
        except Reservation.DoesNotExist:
            # Testy wymagają pustą odpowiedź 404
            return HttpResponse(status=404)

        # Bilet tylko dla potwierdzonych rezerwacji
        if reservation.status != "confirmed":
            return HttpResponse(status=404)

        # Tworzenie QR
        qr_data = f"Reservation:{reservation.id}|Event:{reservation.event.title}"
        qr_img = qrcode.make(qr_data)

        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        buf.seek(0)

        response = HttpResponse(buf.getvalue(), content_type="image/png")
        response["Content-Disposition"] = f'inline; filename="ticket-{reservation.id}.png"'
        return response

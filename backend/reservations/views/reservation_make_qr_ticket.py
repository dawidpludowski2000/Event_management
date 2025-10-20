import io
import qrcode
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from common.exceptions import raise_validation
from reservations.models import Reservation


class ReservationTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, reservation_id: int):
        # znajdź tylko jeśli rezerwacja należy do użytkownika i jest potwierdzona
        try:
            reservation = Reservation.objects.select_related("event").get(
                id=reservation_id, user=request.user
            )
        except Reservation.DoesNotExist:
            raise_validation("Nie masz dostępu do tego biletu.", status=404)

        if reservation.status != "confirmed":
            raise_validation("Bilet dostępny tylko dla potwierdzonych rezerwacji.", status=400)

        qr_data = f"Reservation:{reservation.id}|Event:{reservation.event.title}"
        qr_img = qrcode.make(qr_data)

        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        buf.seek(0)

        response = HttpResponse(buf.getvalue(), content_type="image/png")
        response["Content-Disposition"] = f'inline; filename="ticket-{reservation.id}.png"'
        return response

import qrcode
import io
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from reservations.models import Reservation

class ReservationTicketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, reservation_id):

        try:
            reservation = Reservation.objects.get(id=reservation_id, user=request.user, status="confirmed")
        
        except Reservation.DoesNotExist:
            return HttpResponse(status=404)
        

        qr_data = f"Reservation:{reservation.id}|Event:{reservation.event.title}"
        qr_img = qrcode.make(qr_data)

        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        buf.seek(0)

        return HttpResponse(buf, content_type="image/png")
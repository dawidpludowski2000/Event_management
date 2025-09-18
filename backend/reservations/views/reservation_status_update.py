from django.db import transaction
from events.services.organizer_permissions import IsEventOrganizer
from events.services.realtime_metrics import broadcast_event_metrics
from notifications.services.email import send_reservation_status_email
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from reservations.models import Reservation
from reservations.serializers.reservation_status_update import (
    ReservationStatusUpdateSerializer,
)


class ReservationStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEventOrganizer]

    def patch(self, request, reservation_id: int):
        try:
            reservation = Reservation.objects.select_related("event").get(
                id=reservation_id
            )
        except Reservation.DoesNotExist:
            return Response(
                {"detail": "Zgłoszenie nie istnieje."}, status=status.HTTP_404_NOT_FOUND
            )

        # Nie pozwalamy zmieniać statusu zakończonych zgłoszeń
        if reservation.status in ["confirmed", "rejected"]:
            return Response(
                {"detail": "Nie można zmienić statusu zakończonego zgłoszenia."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ReservationStatusUpdateSerializer(
            instance=reservation, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data.get("status")

        # Limit obowiązuje TYLKO przy potwierdzaniu
        if new_status == "confirmed":
            confirmed_count = Reservation.objects.filter(
                event=reservation.event, status="confirmed"
            ).count()
            if confirmed_count >= reservation.event.seats_limit:
                return Response(
                    {
                        "detail": "Brak wolnych miejsc (limit potwierdzonych osiągnięty)."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Zapisz zmianę atomowo
        with transaction.atomic():
            serializer.save()

        # E-mail z aktualnym (NOWYM) statusem
        send_reservation_status_email(
            user_email=reservation.user.email,
            user_name=reservation.user.get_username() or reservation.user.username,
            event_title=reservation.event.title,
            event_date=reservation.event.start_time,
            status=new_status,
            reply_to=reservation.event.organizer.email,
            event_end=reservation.event.end_time,
            event_location=reservation.event.location,
        )

        broadcast_event_metrics(reservation.event)

        return Response(
            {
                "detail": f"Status zgłoszenia został zmieniony na '{new_status}'.",
                "status": new_status,
            },
            status=200,
        )

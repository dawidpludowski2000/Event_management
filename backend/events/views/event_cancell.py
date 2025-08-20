from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction

from events.models import Event
from reservations.models import Reservation
from events.services.organizer_permissions import IsEventOrganizer


class CancelEventView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEventOrganizer]

    def post(self, request, event_id: int):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"detail": "Event nie istnieje."}, status=status.HTTP_404_NOT_FOUND)

        if event.status == "cancelled":
            return Response({"detail": "Wydarzenie jest już anulowane."}, status=status.HTTP_200_OK)

        with transaction.atomic():
            # 1. Anulowanie wydarzenia
            event.status = "cancelled"
            event.save(update_fields=["status"])

            # 2. Automatyczne odrzucenie powiązanych rezerwacji
            Reservation.objects.filter(
                event=event,
                status__in=["pending", "confirmed"]
            ).update(status="rejected")

        return Response({"detail": "Wydarzenie anulowane, rezerwacje odrzucone."}, status=status.HTTP_200_OK)

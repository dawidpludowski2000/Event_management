
from django.db import transaction
from events.models import Event
from events.services.organizer_permissions import IsEventOrganizer
from events.services.realtime_metrics import broadcast_event_metrics
from reservations.models import Reservation
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.core.api_response import success, error



class CancelEventView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEventOrganizer]

    def post(self, request, event_id: int):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return error("Event nie istnieje.", status=404)

        if event.status == "cancelled":
            return success("Wydarzenie jest już anulowane.")

        with transaction.atomic():
            # 1. Anulowanie wydarzenia
            event.status = "cancelled"
            event.save(update_fields=["status"])

            # 2. Automatyczne odrzucenie powiązanych rezerwacji
            Reservation.objects.filter(
                event=event, status__in=["pending", "confirmed"]
            ).update(status="rejected")

        broadcast_event_metrics(event)

        return success("Wydarzenie anulowane, rezerwacje odrzucone.")

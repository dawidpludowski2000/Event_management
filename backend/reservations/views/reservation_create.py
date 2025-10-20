from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from reservations.serializers.reservation_create import ReservationCreateSerializer
from events.models import Event
from events.services.realtime_metrics import broadcast_event_metrics
from config.core.api_response import success, error
from django.utils import timezone


class ReservationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return error("Wydarzenie nie istnieje.", status=404)

        if event.status != "published":
            return error("To wydarzenie nie jest dostępne do zapisów.", status=400)

        if timezone.now() >= event.start_time:
            return error("Nie można zapisać się na wydarzenie, które już się rozpoczęło.", status=400)

        from reservations.models import Reservation
        if Reservation.objects.filter(user=request.user, event=event).exists():
            return error("Jesteś już zapisany na to wydarzenie.", status=400)

        serializer = ReservationCreateSerializer(
            data={"event": event.id},
            context={"request": request}
        )
        if not serializer.is_valid():
            return error("Błąd walidacji przy tworzeniu rezerwacji.", errors=serializer.errors, status=400)

        reservation = serializer.save()

        broadcast_event_metrics(event)

        return success(
            message="Zgłoszenie zostało wysłane. Czekaj na potwierdzenie.",
            data={"reservation_id": reservation.id},
            status=status.HTTP_201_CREATED
        )

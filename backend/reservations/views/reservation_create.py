from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from reservations.serializers.reservation_create import ReservationCreateSerializer
from events.models import Event
from events.services.realtime_metrics import broadcast_event_metrics
from config.core.api_response import success, error
from django.utils import timezone
from reservations.models import Reservation


class ReservationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        # sprawdź czy event istnieje
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return error(message="Event not found.", status=404)

        # tylko published eventy do zapisów
        if event.status != "published":
            return error(message="This event is not open for registration.", status=400)

        # event już wystartował
        if timezone.now() >= event.start_time:
            return error(message="Registration closed. Event already started.", status=400)

        # user już zapisany
        if Reservation.objects.filter(user=request.user, event=event).exists():
            return error(message="You are already registered for this event.", status=400)

        serializer = ReservationCreateSerializer(
            data={"event": event.id},
            context={"request": request}
        )

        if not serializer.is_valid():
            return error(message="Validation error.", errors=serializer.errors, status=400)

        reservation = serializer.save()

        # broadcast live metric
        broadcast_event_metrics(event)

        return success(
            message="Reservation created. Awaiting confirmation.",
            data={"reservation_id": reservation.id},
            status=status.HTTP_201_CREATED
        )

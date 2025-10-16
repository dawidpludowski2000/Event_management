import logging

from events.models.event import Event
from events.services.realtime_metrics import broadcast_event_metrics
from reservations.serializers.reservation_create import ReservationCreateSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ReservationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response(
                {"detail": "Wydarzenie nie istnieje."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ReservationCreateSerializer(
            data={"event": event.id}, context={"request": request}
        )

        if not serializer.is_valid():
            errors = serializer.errors
            detail = errors.get("detail", ["Validation error"])[0] if isinstance(errors.get("detail"), list) else errors.get("detail", "Validation error")

            return Response(
            {
                "detail": detail,  # ← dla testów i spójności API
                "errors": errors,  # ← oryginalne błędy
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


        serializer.save()

        broadcast_event_metrics(event)

        return Response(
            {"detail": "Rejestracja przebiegła pomyślnie."},
            status=status.HTTP_201_CREATED,
        )

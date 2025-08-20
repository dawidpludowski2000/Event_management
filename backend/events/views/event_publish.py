from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from events.models import Event
from events.services.organizer_permissions import IsEventOrganizer

class PublishEventView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEventOrganizer]

    def post(self, request, event_id: int):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"detail": "Event nie istnieje."}, status=status.HTTP_404_NOT_FOUND)

        if event.status == "published":
            return Response({"detail": "Wydarzenie już jest opublikowane."}, status=status.HTTP_200_OK)

        if event.status == "cancelled":
            return Response({"detail": "Nie można opublikować anulowanego wydarzenia."}, status=status.HTTP_400_BAD_REQUEST)

        if event.end_time <= event.start_time:
            return Response({"detail": "Nieprawidłowy zakres dat (koniec ≤ początek)."}, status=status.HTTP_400_BAD_REQUEST)

        event.status = "published"
        event.save(update_fields=["status"])
        return Response({"detail": "Wydarzenie opublikowane."}, status=status.HTTP_200_OK)

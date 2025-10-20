from events.models import Event
from events.services.organizer_permissions import IsEventOrganizer
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.core.api_response import success, error



class PublishEventView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsEventOrganizer]

    def post(self, request, event_id: int):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return error("Wydarzenie nie istnieje.", status=404)

        if event.status == "published":
            return success("Wydarzenie już jest opublikowane.")
            

        if event.status == "cancelled":
            return Response(
                {"detail": "Nie można opublikować anulowanego wydarzenia."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if event.end_time <= event.start_time:
            return error("Nieprawidłowy zakres dat", status=400)

        event.status = "published"
        event.save(update_fields=["status"])
        return success("Wydarzenie opublikowane.")

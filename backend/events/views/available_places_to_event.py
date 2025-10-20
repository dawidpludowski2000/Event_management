from events.models import Event
from events.serializers.available_places_to_event import AvailablePlacesToEvent
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.core.api_response import success, error


class EventAvailablePlacesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)

        except Event.DoesNotExist:
            return error("Event not found.", status=404)

        serializer = AvailablePlacesToEvent(event)

        return success(data=serializer.data)

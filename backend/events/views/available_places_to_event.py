from events.models import Event
from events.serializers.available_places_to_event import AvailablePlacesToEvent
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class EventAvailablePlacesView(APIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, event_id):

        try:
            event = Event.objects.get(id=event_id)

        except Event.DoesNotExist:

            return Response(
                {"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AvailablePlacesToEvent(event)

        return Response(serializer.data)

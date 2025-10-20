from rest_framework import generics, permissions
from events.models import Event
from events.serializers.event_list import EventListSerializer
from config.core.api_response import success


class OrganizerMyEventsList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventListSerializer

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user).order_by("start_time")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success(data=serializer.data)

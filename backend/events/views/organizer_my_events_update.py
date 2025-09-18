from events.models import Event
from events.serializers.organizer_my_events_update_serializer import (
    EventUpdateSerializer,
)
from rest_framework import generics, permissions


class OrganizerEventUpdateView(generics.RetrieveUpdateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventUpdateSerializer

    def get_queryset(self):

        return Event.objects.filter(organizer=self.request.user)

from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from events.serializers.event_create import EventCreateSerializer
from events.models import Event


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)
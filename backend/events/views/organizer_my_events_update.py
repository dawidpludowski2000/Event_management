from rest_framework import generics, permissions, status
from events.models import Event
from events.serializers.organizer_my_events_update_serializer import EventUpdateSerializer
from config.core.api_response import success, error


class OrganizerEventUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventUpdateSerializer

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        event = self.get_object()
        serializer = self.get_serializer(event)
        return success(data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial = True
        event = self.get_object()
        serializer = self.get_serializer(event, data=request.data, partial=partial)

        if not serializer.is_valid():
            return error("Nieprawidłowe dane.", errors=serializer.errors, status=400)

        serializer.save()
        return success("Wydarzenie zaktualizowane.", data=serializer.data)

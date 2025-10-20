from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from events.models import Event
from events.serializers.event_create import EventCreateSerializer
from config.core.api_response import success, error


class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return error(
                message="Nieprawidłowe dane wydarzenia.",
                errors=serializer.errors,
                status=400
            )

        event = serializer.save(organizer=request.user)
        return success(
            message="Wydarzenie utworzone.",
            data={"id": event.id},
            status=status.HTTP_201_CREATED
        )

from rest_framework import serializers
from events.models.event import Event


class EventListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "location",
            "start_time",
            "end_time",
            "seats_limit",
            "organizer",
            "status"
        ]
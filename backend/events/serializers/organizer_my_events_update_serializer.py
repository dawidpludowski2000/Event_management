from events.models import Event
from rest_framework import serializers


class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["start_time", "description", "seats_limit"]

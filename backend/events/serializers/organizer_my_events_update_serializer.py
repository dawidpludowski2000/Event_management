from rest_framework import serializers
from events.models import Event


class EventUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ["start_time", "description", "seats_limit"]
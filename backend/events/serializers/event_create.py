from rest_framework import serializers
from events.models import Event


class EventCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'start_time', 'end_time', 'seats_limit']


    def validate(self, attrs):
        start = attrs.get("start_time")
        end = attrs.get("end_time")
        limit = attrs.get("seats_limit")

        if limit is not None and limit < 1:
           
            raise serializers.ValidationError({"seats_limit": "Limit miejsc musi być co najmniej 1."})
        
        if start and end and end <= start:
          
            raise serializers.ValidationError({"end_time": "Event nie może zakończyć się przed rozpoczęciem wydarzenia!."})
        
        return attrs
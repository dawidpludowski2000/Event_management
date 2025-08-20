from rest_framework import serializers
from events.models import Event

class AvailablePlacesToEvent(serializers.ModelSerializer):

    confirmed_seats = serializers.SerializerMethodField()    # nie ma w bazie, wyliczam dynamicznie
    spots_left = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ["id", "seats_limit", "confirmed_seats", "spots_left"]


    def get_confirmed_seats(self, obj):
        
        return obj.reservations.filter(status="confirmed").count()
    
    
    def get_spots_left(self, obj):

        return max(0, obj.seats_limit - self.get_confirmed_seats(obj))  # nie może mniej niż 0
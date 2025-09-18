from rest_framework import serializers

from reservations.models import Reservation


class ReservationListSerializer(serializers.ModelSerializer):

    user_email = serializers.EmailField(source="user.email", read_only=True)
    event_title = serializers.CharField(source="event.title", read_only=True)
    event_start_time = serializers.DateTimeField(
        source="event.start_time", read_only=True
    )
    reservation_id = serializers.IntegerField(source="id", read_only=True)
    location = serializers.CharField(source="event.location")

    class Meta:
        model = Reservation
        fields = [
            "reservation_id",
            "user_email",
            "status",
            "created_at",
            "event_title",
            "event_start_time",
            "location",
        ]

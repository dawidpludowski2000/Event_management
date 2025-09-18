from reservations.models import Reservation
from rest_framework import serializers


class ReservationInspectSerializer(serializers.ModelSerializer):
    reservation_id = serializers.IntegerField(source="id", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_first_name = serializers.CharField(source="user.first_name", read_only=True)
    user_last_name = serializers.CharField(source="user.last_name", read_only=True)
    event_id = serializers.IntegerField(source="event.id", read_only=True)
    event_title = serializers.CharField(source="event.title", read_only=True)
    event_start_time = serializers.DateTimeField(
        source="event.start_time", read_only=True
    )

    class Meta:
        model = Reservation
        fields = [
            "reservation_id",
            "status",
            "checked_in",
            "user_email",
            "user_first_name",
            "user_last_name",
            "event_id",
            "event_title",
            "event_start_time",
            "created_at",
        ]

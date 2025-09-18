from rest_framework import serializers

from reservations.models import Reservation


class OrganizerReservationListSerializer(serializers.ModelSerializer):

    reservation_id = serializers.IntegerField(source="id", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    event_title = serializers.CharField(source="event.title", read_only=True)
    event_start_time = serializers.DateTimeField(
        source="event.start_time", read_only=True
    )
    checked_in = serializers.BooleanField(read_only=True)
    event_id = serializers.IntegerField(source="event.id", read_only=True)

    class Meta:

        model = Reservation
        fields = [
            "event_id",
            "reservation_id",
            "user_email",
            "status",
            "checked_in",
            "created_at",
            "event_title",
            "event_start_time",
        ]

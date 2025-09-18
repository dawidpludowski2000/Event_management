from reservations.models import Reservation
from rest_framework import serializers


class ReservationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["status"]

    def validate_status(self, value):
        if value not in ["confirmed", "rejected"]:
            raise serializers.ValidationError(
                "Status może być tylko 'confirmed' lub 'rejected'."
            )

        return value

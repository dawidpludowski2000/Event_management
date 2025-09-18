from django.utils import timezone
from rest_framework import serializers

from reservations.models.reservation import Reservation


class ReservationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ["event", "status"]
        read_only_fields = ["status"]

    def create(self, validated_data):
        user = self.context["request"].user
        event = validated_data["event"]

        if event.status != "published":
            raise serializers.ValidationError(
                {"detail": "To wydarzenie nie jest dostępne do zapisów."}
            )

        if timezone.now() >= event.start_time:
            raise serializers.ValidationError(
                {"detail": "To wydarzenie już się rozpoczęło."}
            )

        if Reservation.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError(
                {"detail": "Użytkownik już zapisał się na to wydarzenie."}
            )

        return Reservation.objects.create(user=user, event=event, status="pending")

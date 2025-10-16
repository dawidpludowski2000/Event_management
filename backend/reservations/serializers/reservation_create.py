from rest_framework import serializers
from reservations.models.reservation import Reservation
from events.models.event import Event
from django.utils import timezone
from common.exceptions import raise_validation  


class ReservationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ["event", "status"]
        read_only_fields = ["status"]

    def create(self, validated_data):
        user = self.context["request"].user
        event = validated_data["event"]

        # Event musi być opublikowany
        if event.status != "published":
            raise_validation("To wydarzenie nie jest dostępne do zapisów.")

        # Nie można zapisać się po rozpoczęciu wydarzenia
        if timezone.now() >= event.start_time:
            raise_validation("To wydarzenie już się rozpoczęło.")

        # Jeden zapis na event
        if Reservation.objects.filter(user=user, event=event).exists():
            raise_validation("Użytkownik już zapisał się na to wydarzenie.")

        return Reservation.objects.create(user=user, event=event, status="pending")

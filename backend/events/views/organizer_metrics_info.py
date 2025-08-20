from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q, F, Value, IntegerField
from events.models import Event

class OrganizerMetricsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = (
            Event.objects
            .filter(organizer=request.user)
            .annotate(
                confirmed_count=Count("reservations", filter=Q(reservations__status="confirmed")),
                pending_count=Count("reservations", filter=Q(reservations__status="pending")),
                checked_in_count=Count("reservations", filter=Q(reservations__checked_in=True)),
            )
            .annotate(
                spots_left=F("seats_limit") - F("confirmed_count")
            )
            .values("id", "title", "start_time", "location",
                    "seats_limit", "confirmed_count", "pending_count",
                    "checked_in_count", "spots_left")
        )
        # max(0, spots_left) w Pythonie:
        data = []
        for row in qs:
            row["spots_left"] = max(0, row["spots_left"])
            data.append(row)
        return Response(data, 200)

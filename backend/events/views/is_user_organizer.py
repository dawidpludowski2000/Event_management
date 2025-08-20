from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from events.models.event import Event


class IsUserOrganizerView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):

        is_organizer = Event.objects.filter(organizer=request.user).exists()

        return Response({"is_organizer": is_organizer})
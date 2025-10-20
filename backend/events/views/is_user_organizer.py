from events.models.event import Event
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.core.api_response import success


class IsUserOrganizerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        
        is_org = Event.objects.filter(organizer=request.user).exists()
        
        return success(data={"is_organizer": is_org})

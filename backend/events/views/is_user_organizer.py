from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class IsUserOrganizerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "success": True,
            "message": "OK",
            "data": {"is_organizer": getattr(request.user, "is_organizer", False)},
        })

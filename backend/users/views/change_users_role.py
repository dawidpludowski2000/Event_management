from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from users.models import CustomUser
from users.serializers.change_users_role import AdminUserSerializer, AdminSetOrganizerSerializer
from config.core.api_response import success, error

class AdminUserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = CustomUser.objects.order_by("-date_joined")
        data = AdminUserSerializer(qs, many=True).data

        return success("User list fetched.", data=data, status=200)


class AdminSetOrganizerView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, user_id: int):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:

            return error("User not found.", status=404)

        serializer = AdminSetOrganizerSerializer(data=request.data)
        if not serializer.is_valid():
            
            return error("Validation error.", errors=serializer.errors, status=400)

        user.is_organizer = serializer.validated_data["is_organizer"]
        user.save(update_fields=["is_organizer"])

        return success(
            "Organizer flag updated.",
            data=AdminUserSerializer(user).data,
            status=status.HTTP_200_OK,
        )

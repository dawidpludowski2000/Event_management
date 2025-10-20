from rest_framework import generics, permissions, status
from users.serializers.user_register import UserRegisterSerializer
from users.models import CustomUser
from config.core.api_response import success, error


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return error(
                message="Nie udało się utworzyć konta.",
                errors=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()

        return success(
            message="Konto utworzone pomyślnie. Sprawdź e-mail aktywacyjny.",
            data={"user_id": user.id, "email": user.email},
            status=status.HTTP_201_CREATED,
        )

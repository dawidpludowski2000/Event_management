from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from config.core.api_response import success, error


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return error(
                message="Nieprawidłowy e-mail lub hasło.",
                status=status.HTTP_401_UNAUTHORIZED
            )

        data = serializer.validated_data
        return success(
            message="Zalogowano pomyślnie.",
            data={
                "access": data.get("access"),
                "refresh": data.get("refresh"),
            },
            status=status.HTTP_200_OK,
        )

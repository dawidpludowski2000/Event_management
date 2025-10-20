from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework import status
from config.core.api_response import success, error


class RefreshTokenView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return error(
                message="Refresh token jest nieprawidłowy lub wygasł.",
                status=status.HTTP_401_UNAUTHORIZED,
            )

        data = serializer.validated_data

        return success(
            message="Token refreshed.",
            data={"access": data.get("access")},
            status=status.HTTP_200_OK
        )

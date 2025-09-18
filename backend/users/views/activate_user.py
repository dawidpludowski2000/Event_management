from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import ActivationToken


class ActivateUserView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, token):
        try:
            token_obj = ActivationToken.objects.select_related("user").get(token=token)
        except ActivationToken.DoesNotExist:
            return Response(
                {"detail": "Nieprawidłowy lub wykorzystany token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = token_obj.user

        if user.is_active:
            return Response(
                {"detail": "Konto jest już aktywne."}, status=status.HTTP_200_OK
            )

        user.is_active = True
        user.save(update_fields=["is_active"])

        # usunięcie wszystkich aktualnych tokenów aktywacyjnych usera
        ActivationToken.objects.filter(user=user).delete()

        return Response(
            {"detail": "Konto zostało aktywowane. Możesz się teraz zalogować."},
            status=status.HTTP_200_OK,
        )

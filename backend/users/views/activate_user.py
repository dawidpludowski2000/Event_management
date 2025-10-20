from rest_framework.views import APIView
from rest_framework import status
from users.models import ActivationToken
from config.core.api_response import success, error


class ActivateUserView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, token):
        try:
            token_obj = ActivationToken.objects.select_related("user").get(token=token)
        except ActivationToken.DoesNotExist:
            return error(
                message="Nieprawidłowy lub wygasły link aktywacyjny.",
                status=status.HTTP_400_BAD_REQUEST
            )

        user = token_obj.user

        if user.is_active:
            # konto już aktywne
            return success(
                message="Konto jest już aktywne. Możesz się zalogować.",
                data={"email": user.email},
                status=status.HTTP_200_OK
            )

        # aktywuj konto
        user.is_active = True
        user.save(update_fields=["is_active"])

        # usuń wszystkie tokeny tego usera
        ActivationToken.objects.filter(user=user).delete()

        return success(
            message="Konto zostało aktywowane. Możesz się teraz zalogować.",
            data={"email": user.email},
            status=status.HTTP_200_OK
        )

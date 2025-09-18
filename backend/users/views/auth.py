from rest_framework import generics, permissions
from users.models import CustomUser
from users.serializers.user_register import UserRegisterSerializer


class RegisterView(generics.CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

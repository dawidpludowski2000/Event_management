from rest_framework import generics, permissions
from users.serializers.user_register import UserRegisterSerializer
from users.models import CustomUser


class RegisterView(generics.CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    

    
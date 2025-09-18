from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, min_length=6)

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all(), message="Ten e-mail już istnieje."
            )
        ]
    )

    class Meta:

        model = CustomUser
        fields = ["email", "first_name", "last_name", "password"]

    def validate_email(self, value: str):
        return value.strip().lower()

    def create(self, validated_data):

        return CustomUser.objects.create_user(**validated_data)

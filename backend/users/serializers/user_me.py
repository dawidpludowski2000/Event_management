from rest_framework import serializers
from users.models import CustomUser

class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "is_staff",
            "is_organizer",
        ]
        read_only_fields = fields

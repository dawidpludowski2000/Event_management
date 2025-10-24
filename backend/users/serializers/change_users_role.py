from rest_framework import serializers
from users.models import CustomUser

class AdminUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name", "is_active", "is_staff", "is_organizer", "date_joined"]
        read_only_fields = ["id", "email", "first_name", "last_name", "is_active", "is_staff", "date_joined"]

class AdminSetOrganizerSerializer(serializers.Serializer):
    is_organizer = serializers.BooleanField()

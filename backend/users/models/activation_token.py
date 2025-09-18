import uuid

from django.db import models
from django.utils import timezone


class ActivationToken(models.Model):
    user = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, related_name="activation_token"
    )
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Token dla {self.user.email} ({self.token})"

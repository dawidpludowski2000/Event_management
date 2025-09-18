from django.db import models
from events.models import Event
from users.models import CustomUser


class Reservation(models.Model):

    STATUS_CHOICES = [
        ("pending", "Oczekuje"),
        ("confirmed", "Potwierdzony"),
        ("rejected", "Odrzucony"),
    ]

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="reservations"
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="reservations"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    checked_in = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "event")

    def __str__(self):
        return f"{self.user.email} → {self.event.title} ({self.status})"

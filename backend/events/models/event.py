from django.db import models
from users.models import CustomUser


class Event(models.Model):

    STATUS_CHOICES = [
        ("draft", "Szkic"),
        ("published", "Opublikowane"),
        ("cancelled", "Anulowane"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    seats_limit = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    organizer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="events"
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="draft")

    def __str__(self):
        return self.title

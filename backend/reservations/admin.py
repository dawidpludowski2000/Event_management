from django.contrib import admin
from reservations.models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["id", "event", "user", "status", "created_at"]
    list_filter = ["status", "event"]
    search_fields = ["user__email", "event__title"]

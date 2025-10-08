import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from users.models import CustomUser  # noqa: E402
from events.models import Event      # noqa: E402


def run():
    print("Seeding demo data...")

    # Użytkownicy
    organizer, created_o = CustomUser.objects.get_or_create(
        email="organizer@example.com",
        defaults={"password": "organizer123"},
    )
    if created_o:
        organizer.set_password("organizer123")
        organizer.is_active = True
        organizer.save()
        print("Created organizer@example.com / organizer123")

    user, created_u = CustomUser.objects.get_or_create(
        email="user@example.com",
        defaults={"password": "user123"},
    )
    if created_u:
        user.set_password("user123")
        user.is_active = True
        user.save()
        print("Created user@example.com / user123")

    # Wydarzenia (muszą mieć czasy i status)
    if not Event.objects.exists():
        now = timezone.now()
        Event.objects.create(
            title="Python Conference 2025",
            description="Demo event for backend testing.",
            location="Warsaw Tech Center",
            start_time=now + timedelta(days=7),
            end_time=now + timedelta(days=7, hours=3),
            seats_limit=50,
            status="published",
            organizer=organizer,
        )
        Event.objects.create(
            title="Music Festival",
            description="Outdoor summer event.",
            location="Cracow Arena",
            start_time=now + timedelta(days=14),
            end_time=now + timedelta(days=14, hours=6),
            seats_limit=100,
            status="published",
            organizer=organizer,
        )
        print("Created demo events.")

    print("✅ Seeding complete.")


if __name__ == "__main__":
    run()

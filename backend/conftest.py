import pytest
from django.db import connection
from django.core.management import call_command
from django.db.models.signals import post_save
import uuid



#  Wyłączam sygnał aktywacji usera w testach (bo generuje śmieci w DB)
@pytest.fixture(autouse=True, scope="session")
def disable_activation_email_signal():
    from users.signals.send_activation_email import send_activation_email  # noqa
    post_save.disconnect(send_activation_email)
    yield
    post_save.connect(send_activation_email)


#  Czyszcze bazę pomiędzy testami (sqlite nie wspiera TRUNCATE)
@pytest.fixture(autouse=True)
def clean_db():
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_keys = OFF;")
        cursor.execute("DELETE FROM users_activationtoken;")
        cursor.execute("DELETE FROM reservations_reservation;")
        cursor.execute("DELETE FROM events_event;")
        cursor.execute("DELETE FROM users_customuser;")
        cursor.execute("PRAGMA foreign_keys = ON;")
    yield


@pytest.fixture
def unique_email():
    """Generuje unikalny email do testów, żeby unikać kolizji w DB."""
    return f"user_{uuid.uuid4().hex[:10]}@example.com"
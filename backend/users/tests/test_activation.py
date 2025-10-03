import uuid
from datetime import timedelta
from unittest.mock import patch

import pytest
from django.test import override_settings
from django.utils import timezone
from events.models import Event
from reservations.models import Reservation
from rest_framework.test import APIClient
from users.models.user import CustomUser
from users.models.activation_token import ActivationToken


@pytest.mark.django_db
@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="test@example.com",
)
def test_user_created_is_inactive_and_token_created(unique_email):
    user = CustomUser.objects.create_user(email=unique_email, password="pass")

    user.refresh_from_db()

    assert user.is_active is False

    assert ActivationToken.objects.filter(user=user).exists() is True


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="test@example.com",
)
@pytest.mark.django_db
def test_activate_endpoint_sets_active_and_removes_tokens(unique_email):
    user = CustomUser.objects.create_user(
        email=unique_email, password="pass"
    )  # signal: inactive + token
    tok = ActivationToken.objects.get(user=user)

    client = APIClient()

    resp = client.get(f"/api/users/activate/{tok.token}/")

    assert resp.status_code == 200
    user.refresh_from_db()
    assert user.is_active is True
    assert not ActivationToken.objects.filter(user=user).exists()


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="test@example.com",
)
@pytest.mark.django_db
def test_activate_with_invalid_token_returns_400(unique_email):
    user = CustomUser.objects.create_user(email=unique_email, password="pass")
    client = APIClient()

    fake_token = uuid.uuid4()  # poprawny format UUID, ale nie istnieje w DB

    resp = client.get(f"/api/users/activate/{fake_token}/")

    assert resp.status_code == 400
    user.refresh_from_db()
    assert user.is_active is False

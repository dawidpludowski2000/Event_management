import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta
from django.test import override_settings

from users.models import CustomUser
from users.models.activation_token import ActivationToken
from events.models import Event
from reservations.models import Reservation


@pytest.mark.django_db
@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="test@example.com",
)
def test_user_created_is_inactive_and_token_created():


    user = CustomUser.objects.create_user(email="u@example.com", password="pass")


    user.refresh_from_db(); assert user.is_active is False

    assert ActivationToken.objects.filter(user=user).exists() is True
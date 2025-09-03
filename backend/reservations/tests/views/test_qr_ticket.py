import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser
from events.models import Event
from reservations.models import Reservation

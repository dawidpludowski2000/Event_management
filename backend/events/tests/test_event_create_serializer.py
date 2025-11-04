from datetime import datetime, timedelta, timezone

import pytest
from events.serializers.event_create import EventCreateSerializer


def _iso_z(dt):
    return (
        dt.astimezone(timezone.utc)
        .replace(microsecond=0)
        .strftime("%Y-%m-%dT%H:%M:%SZ")
    )


@pytest.mark.django_db
def test_end_time_must_be_after_start():
    start = datetime.now(timezone.utc)
    end = start - timedelta(hours=1)  # koniec przed początkiem
    data = {
        "title": "T",
        "location": "Loc",
        "start_time": _iso_z(start),
        "end_time": _iso_z(end),
        "seats_limit": 10,
    }
    serializer = EventCreateSerializer(data=data)
    assert not serializer.is_valid()
    assert "end_time" in serializer.errors or serializer.errors

@pytest.mark.django_db
def test_seats_limit_must_be_positive():
    start = datetime.now(timezone.utc) + timedelta(days=1)
    end = start + timedelta(hours=2)
    data = {
        "title": "T",
        "location": "Loc",
        "start_time": _iso_z(start),
        "end_time": _iso_z(end),
        "seats_limit": 0,  # niepoprawnie
    }
    serializer = EventCreateSerializer(data=data)
    assert not serializer.is_valid()
    assert "seats_limit" in serializer.errors

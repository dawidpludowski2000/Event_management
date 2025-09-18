from datetime import datetime

import pytest
from notifications.services.email import build_event_ics


@pytest.mark.django_db
def test_build_event_ics_has_required_fields():

    title = "Event X"
    location = "Online"
    uid = "user@example.com-EventX-20250905T100000"
    start = datetime(2025, 9, 5, 10, 0, 0)
    end = datetime(2025, 9, 5, 12, 0, 0)

    ics = build_event_ics(title=title, start=start, end=end, location=location, uid=uid)

    # Assert
    assert "BEGIN:VEVENT" in ics
    assert "END:VEVENT" in ics
    assert f"UID:{uid}" in ics
    assert f"SUMMARY:{title}" in ics
    assert f"LOCATION:{location}" in ics
    assert "DTSTART:20250905T100000Z" in ics
    assert "DTEND:20250905T120000Z" in ics


@pytest.mark.django_db
def test_build_event_ics_has_full_structure():

    start = datetime(2025, 9, 5, 10, 0, 0)
    end = datetime(2025, 9, 5, 12, 0, 0)

    # Act
    ics = build_event_ics(
        title="Meeting", start=start, end=end, location="Room 42", uid="abc-123"
    )

    # ICS musi mieć sekcje VCALENDAR i VEVENT w odpowiedniej kolejności
    assert ics.startswith("BEGIN:VCALENDAR")
    assert "BEGIN:VEVENT" in ics
    assert "END:VEVENT" in ics
    assert ics.strip().endswith("END:VCALENDAR")

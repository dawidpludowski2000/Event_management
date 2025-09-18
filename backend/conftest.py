# backend/tests/conftest.py
import uuid
import pytest

@pytest.fixture
def unique_email() -> str:
    """Return a unique, valid email address for tests."""
    return f"user-{uuid.uuid4().hex[:10]}@example.com"

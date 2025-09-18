# backend/tests/utils.py
from uuid import uuid4

def unique_email(prefix: str = "org") -> str:
    return f"{prefix}+{uuid4().hex[:8]}@example.com"

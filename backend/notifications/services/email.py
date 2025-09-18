# notifications/services/email.py
from datetime import datetime, date, time, timezone as dt_timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags
from django.utils import timezone
import logging


def _ensure_datetime(value) -> datetime:
    """Przyjmij datetime lub date i zwróć datetime (00:00 jeśli date)."""
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, time(0, 0))
    raise TypeError(f"Unsupported date type: {type(value)}")


def _format_dt_utc(dt: datetime) -> str:
    """Zwraca datę w formacie ICS, np. 20250901T170000Z (UTC)."""
    dt = _ensure_datetime(dt)
    aware = timezone.make_aware(dt) if timezone.is_naive(dt) else dt
    return aware.astimezone(dt_timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def build_event_ics(*, title: str, start, end, location: str, uid: str) -> str:
    """
    Minimalny plik ICS (VCALENDAR/Vevent) – kompatybilny z Google/Outlook/Apple.
    """
    return (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "PRODID:-//EventFlow//EN\n"
        "CALSCALE:GREGORIAN\n"
        "METHOD:PUBLISH\n"
        "BEGIN:VEVENT\n"
        f"UID:{uid}\n"
        f"SUMMARY:{title}\n"
        f"DTSTART:{_format_dt_utc(start)}\n"
        f"DTEND:{_format_dt_utc(end)}\n"
        f"LOCATION:{location}\n"
        "END:VEVENT\n"
        "END:VCALENDAR\n"
    )


def send_reservation_status_email(
    *,
    user_email: str,
    user_name: str,
    event_title: str,
    event_date,          # datetime/date – start wydarzenia
    status: str,         # "confirmed" | "rejected" | "pending"
    reply_to: str | None = None,
    event_end=None,
    event_location: str = "",
) -> None:
    """
    SRP: złożyć i wysłać wiadomość o zmianie statusu rezerwacji.
    Jeśli status == "confirmed", dołącza plik event.ics (Add to Calendar).
    """

    # --- SOFT GUARD: brak SMTP → nie wysyłaj, ale nie wysadzaj aplikacji ---
    # Testy z locmem backendem dalej przejdą (override_settings w testach).
    if str(getattr(settings, "EMAIL_BACKEND", "")).endswith("smtp.EmailBackend"):
        if not getattr(settings, "EMAIL_HOST", None) or not getattr(settings, "EMAIL_HOST_USER", None):
            
            logger = logging.getLogger(__name__)

            logger.warning("SMTP config missing (EMAIL_HOST/EMAIL_HOST_USER). Skipping send.")

            return

    status = (status or "").strip().lower()

    label_map = {"confirmed": "potwierdzona", "rejected": "odrzucona", "pending": "oczekująca"}
    status_label = label_map.get(status, status)
    subject = f"Twoja rezerwacja: {event_title} – {status_label}"

    html = f"""
    <p>Cześć {user_name},</p>
    <p>Status Twojej rezerwacji na <strong>{event_title}</strong> ({event_date}) został zmieniony na
    <strong>{status_label}</strong>.</p>
    {"<p>Do zobaczenia na wydarzeniu!</p>" if status == "confirmed" else "<p>Przykro nam – tym razem się nie udało.</p>"}
    <p>Pozdrawiamy,<br/>Zespół Events</p>
    """
    text = strip_tags(html)  # prosty plaintext (lepsza dostarczalność)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email],
        reply_to=[reply_to] if reply_to else None,
    )
    msg.attach_alternative(html, "text/html")

    # Dołącz ICS tylko dla potwierdzonych rezerwacji
    if status == "confirmed":
        ics = build_event_ics(
            title=event_title,
            start=event_date,
            end=event_end or event_date,        # ← użyj end jeśli podano
            location=event_location or "",
            uid=f"{user_email}-{event_title}-{str(event_date)}",
        )
        msg.attach(filename="event.ics", content=ics, mimetype="text/calendar")

    msg.send(fail_silently=False)


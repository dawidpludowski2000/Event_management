from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Count, Q
from reservations.models import Reservation


def broadcast_event_metrics(event):
    agg = Reservation.objects.filter(event=event).aggregate(
        confirmed_count=Count("id", filter=Q(status="confirmed")),
        pending_count=Count("id", filter=Q(status="pending")),
        checked_in_count=Count("id", filter=Q(checked_in=True)),
    )
    confirmed = agg["confirmed_count"] or 0
    pending = agg["pending_count"] or 0
    checked_in = agg["checked_in_count"] or 0
    spots_left = max(0, (event.seats_limit or 0) - confirmed)

    payload = {
        "type": "metrics",
        "event_id": event.id,
        "confirmed_count": confirmed,
        "pending_count": pending,
        "checked_in_count": checked_in,
        "spots_left": spots_left,
    }

    print("[DEBUG] broadcast_event_metrics wysyła:", payload)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"event_{event.id}",
        {"type": "event.metrics", "payload": payload},
    )

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from django.db.models import Count, Q
from reservations.models import Reservation
from events.services.realtime_metrics import broadcast_event_metrics


class EventConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            self.event_id = int(self.scope["url_route"]["kwargs"]["event_id"])
        except Exception:
            await self.close()
            return

        self.group_name = f"event_{self.event_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # ⬇️ async bezpieczne wywołanie ORM + broadcast
        await self._send_initial_metrics()

    @sync_to_async
    def _collect_metrics(self):
        agg = Reservation.objects.filter(event_id=self.event_id).aggregate(
            confirmed_count=Count("id", filter=Q(status="confirmed")),
            pending_count=Count("id", filter=Q(status="pending")),
            checked_in_count=Count("id", filter=Q(checked_in=True)),
        )
        confirmed = agg["confirmed_count"] or 0
        pending = agg["pending_count"] or 0
        checked_in = agg["checked_in_count"] or 0
        spots_left = max(0, 50 - confirmed)
        return {
            "type": "metrics",
            "event_id": self.event_id,
            "confirmed_count": confirmed,
            "pending_count": pending,
            "checked_in_count": checked_in,
            "spots_left": spots_left,
        }

    async def _send_initial_metrics(self):
        payload = await self._collect_metrics()
        await self.send_json(payload)

    async def disconnect(self, code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def event_metrics(self, event):
        await self.send_json(event["payload"])

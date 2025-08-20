from channels.generic.websocket import AsyncJsonWebsocketConsumer


# klasa z Django Channels, umożliwiająca pisanie consumer, które obsługują asynchroniczne połączenia (pisanie, odbieranie w: JSON)
class EventConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        # metoda wywoływana automatycznie, gdy klient otwiera połączenie WebSocket
        try:
            self.event_id = int(self.scope["url_route"]["kwargs"]["event_id"])
        except Exception:
            await self.close()
            return

        # każda group to 'pokój' Websocketó, np. event 5
        self.group_name = f"event_{self.event_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Odbiera wiadomości wysyłane przez group_send(type="event.metrics", payload=...)
    async def event_metrics(self, event):
        
        print("[DEBUG] consumer event_metrics:", event.get("payload"))

        await self.send_json(event["payload"])

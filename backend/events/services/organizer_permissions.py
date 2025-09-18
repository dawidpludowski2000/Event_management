# events/permissions.py
from reservations.models import Reservation
from rest_framework.permissions import BasePermission

from events.models import Event


class IsEventOrganizer(BasePermission):
    message = "Nie jesteś organizatorem tego wydarzenia."

    def has_permission(self, request, view):
        # /events/<event_id>/... endpoints
        event_id = view.kwargs.get("event_id")
        if event_id is not None:
            try:
                event = Event.objects.only("id", "organizer_id").get(pk=event_id)
            except Event.DoesNotExist:
                return False
            view._event = event
            return event.organizer_id == request.user.id

        # /reservations/<reservation_id>/... endpoints
        reservation_id = view.kwargs.get("reservation_id")
        if reservation_id is not None:
            try:
                res = (
                    Reservation.objects.select_related("event")
                    .only("id", "event__organizer_id")
                    .get(pk=reservation_id)
                )
            except Reservation.DoesNotExist:
                return False
            view._reservation = res
            view._event = res.event
            return res.event.organizer_id == request.user.id

        return True

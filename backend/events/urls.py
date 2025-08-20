from django.urls import path
from events.views.event_create import EventCreateView
from events.views.event_list import EventListView
from events.views.is_user_organizer import IsUserOrganizerView
from events.views.available_places_to_event import EventAvailablePlacesView
from events.views.organizer_my_events_list import OrganizerMyEventsList
from events.views.organizer_my_events_update import OrganizerEventupdateView
from events.views.event_publish import PublishEventView
from events.views.event_cancel import CancelEventView
from events.views.organizer_metrics_info import OrganizerMetricsView

urlpatterns = [
    # Publiczna lista wydarzeń (tylko opublikowane)
    path("", EventListView.as_view(), name="event-list"),

    # Dostępność miejsc na wydarzeniu (public)
    path("<int:event_id>/availability/", EventAvailablePlacesView.as_view(), name="event-available-seats"),

    # Sprawdzenie, czy zalogowany user jest organizatorem jakiegokolwiek eventu (na potrzeby UI)
    path("is-organizer/", IsUserOrganizerView.as_view(), name="is-organizer"),

    # Organizator: utwórz wydarzenie (domyślnie draft)
    path("organizer/events/create/", EventCreateView.as_view(), name="organizer-event-create"),

    # Organizator: lista moich wydarzeń
    path("organizer/my-events-list/", OrganizerMyEventsList.as_view(), name="organizer-events-list"),

    # Organizator: edycja mojego wydarzenia
    path("organizer/<int:event_id>/edit/", OrganizerEventupdateView.as_view(), name="organizer-event-update"),

    # Organizator: publikacja wydarzenia
    path("organizer/<int:event_id>/publish/", PublishEventView.as_view(), name="organizer-event-publish"),

    # Organizator: anulowanie wydarzenia
    path("organizer/<int:event_id>/cancel/", CancelEventView.as_view(), name="organizer-event-cancel"),

    # Organizator: lista eventów dla organizatora z licznikami
    path("organizer/metrics/", OrganizerMetricsView.as_view(), name="organizer-metrics"),
]

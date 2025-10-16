from django.urls import path
from reservations.views.cancel_my_reservation import CancelMyReservationView
from reservations.views.my_reservation import MyReservationsView
from reservations.views.my_single_reservation_detail import (
    MySingleReservationDetailView,
)
from reservations.views.organizer_reservation_check_in_ticket import (
    OrganizerReservationCheckInView,
)
from reservations.views.organizer_reservation_list import OrganizerReservationView
from reservations.views.reservation_create import ReservationCreateView
from reservations.views.reservation_inspect_organizer import (
    OrganizerReservationInspectView,
)
from reservations.views.reservation_list import ParticipantsListView
from reservations.views.reservation_make_qr_ticket import ReservationTicketView
from reservations.views.reservation_status_update import ReservationStatusUpdateView

urlpatterns = [
    # Rejestracja na wydarzenie
    path(
        "events/<int:event_id>/register/",
        ReservationCreateView.as_view(),
        name="event-register",
    ),
    # Lista uczestników wydarzenia (dla organizatora)
    path(
        "events/<int:event_id>/participants/",
        ParticipantsListView.as_view(),
        name="event-participants",
    ),
    # Szczegóły mojej rezerwacji dla konkretnego eventu
    path(
        "events/<int:event_id>/my-reservation/",
        MySingleReservationDetailView.as_view(),
        name="my-single-reservation-detail",
    ),
    # Zmiana statusu rezerwacji (organizator potwierdza/odrzuca)
    path(
        "reservations/<int:reservation_id>/status/",
        ReservationStatusUpdateView.as_view(),
        name="reservation-status-update",
    ),
    # Lista wszystkich moich rezerwacji (użytkownik)
    path("my-reservations/", MyReservationsView.as_view(), name="my-reservations"),
    # Lista wszystkich rezerwacji w moich wydarzeniach (organizator)
    path(
        "organizer/reservations/",
        OrganizerReservationView.as_view(),
        name="organizer-reservation",
    ),
    # Anulowanie własnej rezerwacji
    path(
        "reservations/<int:reservation_id>/",
        CancelMyReservationView.as_view(),
        name="cancel-my-reservation",
    ),
    # Pobranie biletu QR
    path(
        "reservations/<int:reservation_id>/ticket/",
        ReservationTicketView.as_view(),
        name="reservation-ticket",
    ),
    # Check-in po zeskanowaniu biletu (organizator)
    path(
        "reservations/<int:reservation_id>/check-in/",
        OrganizerReservationCheckInView.as_view(),
        name="reservation-check-in",
    ),
    # Sprawdzanie rezerwacji, informacje
    path(
        "reservations/<int:reservation_id>/inspect/",
        OrganizerReservationInspectView.as_view(),
        name="reservation-inspect",
    ),
]

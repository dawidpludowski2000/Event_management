from django.urls import path
from users.views.refresh import RefreshTokenView
from users.views.activate_user import ActivateUserView
from users.views.auth import RegisterView
from users.views.login import LoginView
from users.views.change_users_role import AdminUserListView
from users.views.change_users_role import AdminSetOrganizerView
from users.views.me_view import MeView



urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    path("activate/<uuid:token>/", ActivateUserView.as_view(), name="activate-user"),
    path("admin/users/", AdminUserListView.as_view(), name="admin-user-list"),
    path("admin/users/<int:user_id>/set-organizer/", AdminSetOrganizerView.as_view(), name="admin-set-organizer"),
    path("me/", MeView.as_view(), name="me"),
]

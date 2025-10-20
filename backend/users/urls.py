from django.urls import path
from users.views.refresh import RefreshTokenView
from users.views.activate_user import ActivateUserView
from users.views.auth import RegisterView
from users.views.login import LoginView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    path("activate/<uuid:token>/", ActivateUserView.as_view(), name="activate-user"),
]

from django.urls import path
from users.views.auth import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views.activate_user import ActivateUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/<uuid:token>/', ActivateUserView.as_view(), name='activate-user'),
]

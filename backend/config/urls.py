"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from config.views.health import healthcheck
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# --- v1 package ---
api_v1_patterns = [
    path("users/", include("users.urls")),
    path("events/", include("events.urls")),
    path("", include("reservations.urls")),
    path("login/", TokenObtainPairView.as_view(), name="login_v1"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair_v1"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh_v1"),
    path("schema/", SpectacularAPIView.as_view(), name="schema_v1"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema_v1"),
        name="swagger_ui_v1",
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema_v1"), name="redoc_v1"),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    # --- legacy (działa jak dotąd) ---
    path("api/users/", include("users.urls")),
    path("api/events/", include("events.urls")),
    path("api/", include("reservations.urls")),
    path("api/login/", TokenObtainPairView.as_view(), name="login"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("health/", healthcheck, name="health"),
    # --- oficjalne v1 ---
    path("api/v1/", include((api_v1_patterns, "apiv1"))),
]

# --- SENTRY TEST ENDPOINT ---
def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns += [
    path("sentry-debug/", trigger_error),
]

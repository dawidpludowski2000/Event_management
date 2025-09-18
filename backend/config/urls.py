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

import os

import redis
from django.contrib import admin
from django.db import connection
from django.http import JsonResponse
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


def healthcheck(request):
    db_ok = True
    redis_ok = True

    # DB check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()
    except Exception:
        db_ok = False

    # Redis check (opcjonalnie)
    try:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        r = redis.Redis.from_url(redis_url)
        r.ping()
    except Exception:
        redis_ok = False

    status = 200 if (db_ok and redis_ok) else 503
    return JsonResponse(
        {"status": "ok" if status == 200 else "fail", "db": db_ok, "redis": redis_ok},
        status=status,
    )


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

"""
Django settings for EventFlow (clean PRO).
"""

from __future__ import annotations

import os
from pathlib import Path
from datetime import timedelta
import sys

from dotenv import load_dotenv
import dj_database_url

# -----------------------------------------------------------------------------
# Base
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()  # pozwala korzystać z .env lokalnie

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-insecure-key")
DEBUG = os.getenv("DEBUG", "True") == "True"

# ALLOWED_HOSTS – jeśli env puste, w DEV fallback na localhost
_env_hosts = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()]
ALLOWED_HOSTS = _env_hosts or (["localhost", "127.0.0.1"] if DEBUG else [])

# Dodajemy testserver dla pytesta
if "testserver" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("testserver")

# -----------------------------------------------------------------------------
# Apps
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local apps
    "users.apps.UsersConfig",
    "events",
    "reservations",
    "notifications",

    # Third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "corsheaders",
    "channels",
    "drf_spectacular",
]

# -----------------------------------------------------------------------------
# Middleware
# -----------------------------------------------------------------------------
MIDDLEWARE = [
    # CORS na górze
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # Request ID → w logach
    "config.core.request_id.RequestIDMiddleware",
    # Globalny response-wrapper middleware (opcjonalnie, mamy renderer)
    # "config.core.response_wrapper.ResponseWrapperMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------
DEFAULT_SQLITE_URL = f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=False,
    )
}

# --- Test DB isolation (pytest fix: duplicate emails, clean DB per test run)
DATABASES["default"]["TEST"] = {"NAME": ":memory:"}


# -----------------------------------------------------------------------------
# Auth / User model
# -----------------------------------------------------------------------------
AUTH_USER_MODEL = "users.CustomUser"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------------------------------------------------------
# i18n / tz
# -----------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------------------------
# Static
# -----------------------------------------------------------------------------
STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------------------------------------------------------
# CORS / CSRF
# -----------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()
]
# DEV fallback: jeśli nie podano, a DEBUG=True → pozwól na wszystko
CORS_ALLOW_ALL_ORIGINS = bool(DEBUG and not CORS_ALLOWED_ORIGINS)

# Jeżeli korzystasz z cookies (my mamy JWT w headerze – nie jest wymagane)
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "False") == "True"

CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
]

# -----------------------------------------------------------------------------
# DRF
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "config.core.exceptions.custom_exception_handler",

    # Globalny JSON envelope
    "DEFAULT_RENDERER_CLASSES": (
        "config.core.renderers.EnvelopeJSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),

    # Throttling (base)
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/day",
        "user": "1000/day",
        # "login": "5/minute",  # jeżeli dodasz osobny throttler na login
    },

    
}

# Disable throttling during tests
if "test" in sys.argv:
    REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []
    REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {}


SPECTACULAR_SETTINGS = {
    "TITLE": "EventFlow API",
    "DESCRIPTION": "API for EventFlow - events, reservations, organizers",
    "VERSION": "1.0.0",
}

# -----------------------------------------------------------------------------
# JWT (SIMPLE_JWT)
# -----------------------------------------------------------------------------
ACCESS_TOKEN_MIN = int(os.getenv("ACCESS_TOKEN_LIFETIME_MINUTES", "60"))
REFRESH_TOKEN_DAYS = int(os.getenv("REFRESH_TOKEN_LIFETIME_DAYS", "7"))

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_TOKEN_MIN),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_TOKEN_DAYS),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# -----------------------------------------------------------------------------
# Channels (WebSockets)
# -----------------------------------------------------------------------------
REDIS_URL = os.getenv("REDIS_URL", "").strip()
if REDIS_URL:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {"hosts": [REDIS_URL]},
        }
    }
else:
    CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

# -----------------------------------------------------------------------------
# Email
# -----------------------------------------------------------------------------
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "EventFlow <no-reply@example.com>")

# W DEV wymuś konsolę niezależnie od env
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# -----------------------------------------------------------------------------
# Version / build metadata (opcjonalne)
# -----------------------------------------------------------------------------
APP_VERSION = os.getenv("APP_VERSION")
if not APP_VERSION:
    try:
        with open(BASE_DIR / "VERSION", "r", encoding="utf-8") as f:
            APP_VERSION = f.read().strip()
    except Exception:
        APP_VERSION = "0.0.0"

GIT_COMMIT = os.getenv("GIT_COMMIT", "")
BUILD_TIME = os.getenv("BUILD_TIME", "")

# -----------------------------------------------------------------------------
# Logging (PRO) – z request_id i trybem JSON
# -----------------------------------------------------------------------------
LOG_JSON = os.getenv("LOG_JSON", "False") == "True"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_id": {"()": "config.core.logging.RequestIDLogFilter"},
    },
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {name} rid={request_id} : {message}",
            "style": "{",
        },
        "json": {
            "format": '{{"time":"{asctime}","level":"{levelname}","logger":"{name}","rid":"{request_id}","msg":"{message}"}}',
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["request_id"],
            "formatter": "json" if LOG_JSON else "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# -----------------------------------------------------------------------------
# Security headers (toggle w PROD)
# -----------------------------------------------------------------------------
# Bazowe (zawsze rozsądne)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

ENABLE_SECURE_HEADERS = os.getenv("ENABLE_SECURE_HEADERS", "False") == "True"
if ENABLE_SECURE_HEADERS:
    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True") == "True"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "True") == "True"
    CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "True") == "True"
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", "True") == "True"
    SECURE_HSTS_PRELOAD = os.getenv("SECURE_HSTS_PRELOAD", "True") == "True"
    SECURE_REFERRER_POLICY = os.getenv("SECURE_REFERRER_POLICY", "strict-origin-when-cross-origin")

# -----------------------------------------------------------------------------
# Sentry (opcjonalnie)
# -----------------------------------------------------------------------------
SENTRY_DSN = os.getenv("SENTRY_DSN", "").strip()
if SENTRY_DSN:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration

        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[DjangoIntegration()],
            traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.0")),
            profiles_sample_rate=float(os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "0.0")),
            send_default_pii=True,
            environment=os.getenv("SENTRY_ENVIRONMENT", "local"),
            release=APP_VERSION,
        )
    except Exception as e:  # pragma: no cover
        import logging
        logging.getLogger(__name__).warning("Sentry init skipped: %s", e)

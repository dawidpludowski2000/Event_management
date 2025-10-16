from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.exceptions import ValidationError, PermissionDenied, NotAuthenticated


def custom_exception_handler(exc, context):
    """
    Global JSON exception handler – unified error format.
    """
    drf_response = exception_handler(exc, context)

    # Standardowe wyjątki Django/DRF
    if isinstance(exc, Http404):
        return _error("Not found", status.HTTP_404_NOT_FOUND)

    if isinstance(exc, NotAuthenticated):
        return _error("Authentication required", status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, PermissionDenied):
        return _error("Permission denied", status.HTTP_403_FORBIDDEN)

    if isinstance(exc, ValidationError):
        return _error("Validation error", status.HTTP_400_BAD_REQUEST, exc.detail)

    # Reszta wyjątków obsłużona przez DRF
    if drf_response is not None:
        detail = drf_response.data.get("detail", "Server error")
        return _error(detail, drf_response.status_code, drf_response.data)

    # Nieobsłużone błędy (500)
    return _error("Internal server error", status.HTTP_500_INTERNAL_SERVER_ERROR)


def _error(message, status_code, errors=None):
    """
    Helper to return a unified error JSON response.
    """
    return Response(
        {
            "success": False,
            "message": message,
            "errors": errors or {},
        },
        status=status_code,
    )

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.exceptions import ValidationError, PermissionDenied, NotAuthenticated


def custom_exception_handler(exc, context):
    """
    Global JSON error handler – returns uniform error responses.
    """
    response = exception_handler(exc, context)

    if isinstance(exc, Http404):
        return Response(
            {"success": False, "message": "Not found", "errors": None},
            status=status.HTTP_404_NOT_FOUND,
        )

    if isinstance(exc, NotAuthenticated):
        return Response(
            {"success": False, "message": "Authentication required", "errors": None},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if isinstance(exc, PermissionDenied):
        return Response(
            {"success": False, "message": "Permission denied", "errors": None},
            status=status.HTTP_403_FORBIDDEN,
        )

    if isinstance(exc, ValidationError):
        return Response(
            {
                "success": False,
                "message": "Validation error",
                "errors": exc.detail,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if response is not None:
        return Response(
            {
                "success": False,
                "message": response.data.get("detail", "Server error"),
                "errors": None,
            },
            status=response.status_code,
        )

    # Unhandled exceptions (500)
    return Response(
        {"success": False, "message": "Internal server error", "errors": None},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

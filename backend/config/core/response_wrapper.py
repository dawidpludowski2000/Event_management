import json
from django.http import JsonResponse, HttpResponseBase
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


class ResponseWrapperMiddleware(MiddlewareMixin):
    def process_response(self, request, response: HttpResponseBase):
        # Tylko /api/
        if not request.path.startswith("/api/"):
            return response

        # Jeśli to ValidationError – NIE ruszać, testy tego wymagają
        if isinstance(getattr(response, "data", None), dict) and "detail" in response.data:
            return response  # ✅ zostawiamy jak jest

        # Jeśli brak .data – zostawiamy
        if not hasattr(response, "data"):
            return response

        # Jeśli już opakowane – zostawiamy
        if isinstance(response.data, dict) and "success" in response.data:
            return response

        status = response.status_code

        # Sukces
        if 200 <= status < 300:
            return JsonResponse({
                "success": True,
                "message": response.data.get("detail", "OK") if isinstance(response.data, dict) else "OK",
                "data": response.data
            }, status=status)

        # Błąd ogólny
        return JsonResponse({
            "success": False,
            "message": response.data.get("message") if isinstance(response.data, dict) else "Request failed",
            "errors": response.data
        }, status=status)

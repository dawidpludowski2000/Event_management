import json
from django.http import JsonResponse, HttpResponseBase
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response


class ResponseWrapperMiddleware(MiddlewareMixin):
   
    def process_response(self, request, response: HttpResponseBase):

        # Only wrap API endpoints starting with /api/
        if not request.path.startswith("/api/"):
            return response

        # Skip non-DRF / non-JSON responses
        if not hasattr(response, "data"):
            return response

        # Avoid double wrapping – if already wrapped, skip
        if isinstance(response.data, dict) and "success" in response.data:
            return response

        status = response.status_code

        # SUCCESS (2xx)
        if 200 <= status < 300:
            wrapped = {
                "success": True,
                "message": response.data.get("detail", "OK") if isinstance(response.data, dict) else "OK",
                "data": response.data,
            }
            return JsonResponse(wrapped, status=status)

        # ERROR
        error_message = None
        if isinstance(response.data, dict):
            error_message = response.data.get("detail") or response.data.get("message")

        wrapped = {
            "success": False,
            "message": error_message or "Request failed",
            "errors": response.data,
        }

        return JsonResponse(wrapped, status=status)

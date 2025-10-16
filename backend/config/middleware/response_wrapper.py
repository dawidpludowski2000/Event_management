from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import json

class ResponseWrapperMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if not request.path.startswith("/api/"):
            return response

        try:
            data = json.loads(response.content.decode())
        except Exception:
            return response

        status = response.status_code

        if 200 <= status < 400:
            return JsonResponse({
                "success": True,
                "message": data.get("detail", "OK"),
                "data": data
            }, status=status)

        detail = data.get("detail") or data.get("message") or "Request failed"

        return JsonResponse({
            "success": False,
            "message": detail,
            "detail": detail,  
            "errors": data     
        }, status=status)

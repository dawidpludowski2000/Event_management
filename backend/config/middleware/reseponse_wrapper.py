from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
import logging

log = logging.getLogger(__name__)

class ResponseWrapperMiddleware(MiddlewareMixin):
    def process_response(self, request, response: HttpResponse) -> HttpResponse:
        if request.path.startswith("/api/"):
            log.info("[respwrap-min] %s %s -> %s",
                     request.method, request.path, getattr(response, "status_code", "?"))
        return response

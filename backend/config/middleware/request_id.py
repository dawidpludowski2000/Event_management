import uuid
from django.utils.deprecation import MiddlewareMixin
from config.logging import request_id_var

class RequestIDMiddleware(MiddlewareMixin):
    """
    Ustawia unikalny X-Request-ID na każdym żądaniu.
    Jeśli klient dostarczył X-Request-ID, to go zachowujemy.
    """
    HEADER_NAME = "HTTP_X_REQUEST_ID"   # w request.META
    RESPONSE_HEADER = "X-Request-ID"    # w odpowiedzi

    def process_request(self, request):
        rid = request.META.get(self.HEADER_NAME)
        if not rid:
            rid = str(uuid.uuid4())
        request.request_id = rid
        request_id_var.set(rid)

        
        try:
            import sentry_sdk
            rid = request_id_var.get("-")
            with sentry_sdk.configure_scope() as scope:
                scope.set_tag("request_id", rid)
        except Exception:
            pass
        

        return None

    def process_response(self, request, response):
        rid = getattr(request, "request_id", None)
        if rid:
            response[self.RESPONSE_HEADER] = rid
        return response

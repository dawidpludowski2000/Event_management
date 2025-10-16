from rest_framework.renderers import JSONRenderer
from collections.abc import Mapping


class EnvelopeJSONRenderer(JSONRenderer):
    """
    Opakowuje TYLKO odpowiedzi DRF w jednolity format.

    2xx:
      { "success": true,  "message": "OK", "data": <payload> }

    4xx/5xx:
      { "success": false, "message": "<reason>", "errors": <raw> }

    Jeśli widok sam zwróci strukturę z kluczem 'success' – nic nie zmieniamy.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None
        request = renderer_context.get("request") if renderer_context else None

        # Jeżeli już jest nasza koperta – nic nie ruszamy
        if isinstance(data, Mapping) and "success" in data:
            return super().render(data, accepted_media_type, renderer_context)

        # Tylko API DRF (gdy response istnieje)
        if response is None:
            return super().render(data, accepted_media_type, renderer_context)

        status = getattr(response, "status_code", 200)
        is_error = status >= 400

        # message: spróbuj wziąć z 'detail', inaczej default
        message = None
        if isinstance(data, Mapping):
            detail = data.get("detail")
            if isinstance(detail, str):
                message = detail

        if is_error:
            envelope = {
                "success": False,
                "message": message or response.status_text or "Error",
                "errors": data,
            }
        else:
            envelope = {
                "success": True,
                "message": message or "OK",
                "data": data,
            }

        return super().render(envelope, accepted_media_type, renderer_context)

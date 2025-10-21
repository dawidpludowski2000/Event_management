from rest_framework.throttling import SimpleRateThrottle

class LoginRateThrottle(SimpleRateThrottle):
    scope = "login"

    def get_cache_key(self, request, view):
        if request.method != "POST":
            return None
        # identyfikujemy użytkownika po IP
        return self.get_ident(request)

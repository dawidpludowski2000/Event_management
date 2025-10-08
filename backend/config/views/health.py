from django.http import JsonResponse
from django.db import connections
from django.conf import settings
import redis
import os


def healthcheck(request):
    db_ok = True
    redis_ok = True

    # DB check
    try:
        connections["default"].cursor()
    except Exception:
        db_ok = False

    # Redis check
    try:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        r = redis.Redis.from_url(redis_url)
        r.ping()
    except Exception:
        redis_ok = False

    status_code = 200 if db_ok and redis_ok else 503
    payload = {
        "status": "ok" if status_code == 200 else "fail",
        "db_ok": db_ok,        # możesz zostawić stare nazwy 'db'/'redis' jeśli wolisz
        "redis_ok": redis_ok,
        "version": getattr(settings, "APP_VERSION", "0.0.0"),
        "commit": getattr(settings, "GIT_COMMIT", ""),
        "build_time": getattr(settings, "BUILD_TIME", ""),
    }
    return JsonResponse(payload, status=status_code)

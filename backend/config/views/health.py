import os

import redis
from django.db import connections
from django.http import JsonResponse


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

    status = 200 if db_ok and redis_ok else 503
    return JsonResponse(
        {"status": "ok" if status == 200 else "fail", "db": db_ok, "redis": redis_ok},
        status=status,
    )

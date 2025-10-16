import os
import logging

SENTRY_DSN = os.getenv("SENTRY_DSN", "").strip()
SENTRY_ENVIRONMENT = os.getenv("SENTRY_ENVIRONMENT", "development")
SENTRY_TRACES_SAMPLE_RATE = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.0"))
SENTRY_PROFILES_SAMPLE_RATE = float(os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "0.0"))

def init_sentry():
    if not SENTRY_DSN:
        logging.getLogger(__name__).info("[Sentry] DSN empty — Sentry disabled.")
        return

    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=SENTRY_ENVIRONMENT,
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(
                level=logging.INFO,        # capture info+ as breadcrumbs
                event_level=logging.ERROR  # send events for ERROR+
            ),
        ],
        send_default_pii=True,
        traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
        profiles_sample_rate=SENTRY_PROFILES_SAMPLE_RATE,
    )

    logging.getLogger(__name__).info(
        "[Sentry] Initialized (env=%s, traces=%s, profiles=%s)",
        SENTRY_ENVIRONMENT, SENTRY_TRACES_SAMPLE_RATE, SENTRY_PROFILES_SAMPLE_RATE
    )

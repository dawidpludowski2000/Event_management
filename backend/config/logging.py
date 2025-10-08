import logging
from contextvars import ContextVar

# Context var do przenoszenia request_id do logów
request_id_var: ContextVar[str] = ContextVar("request_id", default="-")

class RequestIDLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get("-")
        return True

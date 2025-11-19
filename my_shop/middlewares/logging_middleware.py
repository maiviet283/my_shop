import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("django.request")

EXCLUDED_PATHS = (
    "/static/",
    "/media/",
    "/favicon.ico",
)

class RequestResponseLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if any(request.path.startswith(p) for p in EXCLUDED_PATHS):
            request._skip_logging = True
            return

        request._start_time = time.time()

    def process_response(self, request, response):
        if getattr(request, "_skip_logging", False):
            return response

        duration = None
        if hasattr(request, "_start_time"):
            duration = (time.time() - request._start_time) * 1000

        log_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "type": "response",
            "method": request.method,
            "path": request.path,
            "status_code": response.status_code,
            "duration_ms": round(duration, 2) if duration else None,
            "content_length": len(getattr(response, "content", b"")),
            "user": {"authenticated": request.user.is_authenticated},
            "ip": request.META.get("REMOTE_ADDR"),
        }

        logger.info("request log", extra={"extra": log_data})
        return response

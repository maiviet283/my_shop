import time
import re
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("django.request")

SQLI_PATTERNS = [
    r"(?i)(union(\s+all)?)\s+select",
    r"(?i)or\s+1=1",
    r"(?i)and\s+1=1",
    r"(?i)information_schema",
    r"(?i)sleep\(\d+\)",
    r"(?i)benchmark\(",
    r"'--",
    r"\"--",
]

XSS_PATTERNS = [
    r"(?i)<script",
    r"(?i)onerror=",
    r"(?i)onclick=",
    r"(?i)javascript:",
]

class AdvancedSecurityLoggingMiddleware(MiddlewareMixin):

    def detect_attack(self, text: str):
        if not text:
            return None

        for p in SQLI_PATTERNS:
            if re.search(p, text):
                return "sql_injection"

        for p in XSS_PATTERNS:
            if re.search(p, text):
                return "xss"

        return None

    def process_request(self, request):
        request._start_time = time.time()

        if request.method in ("POST", "PUT", "PATCH"):
            try:
                request._body_data = request.body.decode("utf-8", errors="ignore")
            except:
                request._body_data = None
        else:
            request._body_data = None

        return None

    def process_response(self, request, response):
        duration = round((time.time() - request._start_time) * 1000, 2)

        full_path = request.get_full_path()
        query_params = request.META.get("QUERY_STRING", "")
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        ip = request.META.get("REMOTE_ADDR") or request.META.get("HTTP_X_FORWARDED_FOR")

        body = getattr(request, "_body_data", None)

        # Detect attack
        combined_text = " ".join([
            str(full_path), str(query_params), str(body or "")
        ])

        attack_type = self.detect_attack(combined_text)

        log_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "method": request.method,
            "path": request.path,
            "full_path": full_path,
            "query_params": query_params,
            "body": body[:500] if body else None,
            "status_code": response.status_code,
            "duration_ms": duration,
            "content_length": len(getattr(response, "content", b"")),
            "user": {
                "authenticated": request.user.is_authenticated,
                "username": str(request.user) if request.user.is_authenticated else None,
            },
            "ip": ip,
            "user_agent": user_agent,
            "attack": attack_type,
            "type": "suspicious" if attack_type else "normal",
        }

        if attack_type:
            logger.warning("possible attack", extra={"extra": log_data})
        else:
            logger.info("normal request", extra={"extra": log_data})

        return response

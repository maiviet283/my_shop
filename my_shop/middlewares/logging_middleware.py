import time
import re
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("django.request")


SQLI_PATTERNS = [

    # UNION
    r"(?i)(union(\s+all)?)\s+select",
    r"(?i)union\s+distinct\s+select",

    # Boolean-based
    r"(?i)\b(or|and)\b\s+\d+=\d+",
    r"(?i)\b(or|and)\b\s+'[^']*'='[^']*'",
    r"(?i)\b(or|and)\b\s+true\b",
    r"(?i)\b(or|and)\b\s+false\b",

    # Comment-based
    r"(?i)--\s",
    r"(?i)#\s",
    r"(?i)/\*.*\*/",

    # Tautologies
    r"(?i)('\s*or\s*'1'='1)",
    r"(?i)(\"\s*or\s*\"1\"=\"1)",
    r"(?i)\b1=1\b",
    r"(?i)\b1=0\b",

    # Stacked queries
    r"(?i);[\s]*(drop|select|insert|update|delete|truncate|exec|execute)\b",
    r"(?i)';\s*(drop|select|insert|update|delete|truncate|exec)",

    # Time-based injections
    r"(?i)sleep\(\s*\d+\s*\)",
    r"(?i)benchmark\s*\(",
    r"(?i)pg_sleep\(",
    r"(?i)waitfor\s+delay\s+'",

    # Information schema / metadata
    r"(?i)information_schema",
    r"(?i)pg_catalog",
    r"(?i)sys\.tables",
    r"(?i)sys\.columns",
    r"(?i)mysql\.user",

    # Function exploits
    r"(?i)load_file\s*\(",
    r"(?i)into\s+outfile",
    r"(?i)group_concat\s*\(",

    # Type casting
    r"(?i)cast\s*\(",
    r"(?i)convert\s*\(",

    # Hex / encoded payloads
    r"(?i)0x[0-9a-fA-F]+",
    r"(?i)char\(\s*\d+",

    # Special operators
    r"(?i)regexp\s+'",
    r"(?i)rlike\s+",

    # OR 1=1 variants
    r"(?i)\bor\b\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+['\"]?",
    r"(?i)\band\b\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+['\"]?",
]


XSS_PATTERNS = [

    # script tags
    r"(?i)<\s*script",
    r"(?i)<script[^>]*>",
    r"(?i)<script[\s\S]*?>[\s\S]*?</script>",

    # event handlers
    r"(?i)on\w+\s*=",
    r"(?i)onload=",
    r"(?i)onerror=",
    r"(?i)onclick=",
    r"(?i)onmouseover=",
    r"(?i)onfocus=",

    # javascript: URI
    r"(?i)javascript:",
    r"(?i)vbscript:",
    r"(?i)data:\s*text\/html",

    # img-based XSS
    r"(?i)<img[^>]+src\s*=\s*['\"]javascript:",
    r"(?i)<img[^>]+onerror=",

    # iframe, object
    r"(?i)<iframe",
    r"(?i)<object",
    r"(?i)<embed",

    # malicious input tags
    r"(?i)<input[^>]+on\w+=",

    # encoded payloads
    r"(?i)%3Cscript",
    r"(?i)%3Cimg",
    r"(?i)%3Ciframe",
    r"(?i)&#x3C;script",
    r"(?i)&#x3C;img",

    # CSS-based XSS
    r"(?i)expression\s*\(",
    r"(?i)url\(\s*['\"]?javascript:",

    # malformed tag injection
    r"(?i)<\s*svg",
    r"(?i)<\s*math",
    r"(?i)<\s*xss",

    # document / window access
    r"(?i)document\.cookie",
    r"(?i)document\.write",
    r"(?i)window\.location",
    r"(?i)window\.onload",

    # prototype pollution style
    r"(?i)__proto__",
    r"(?i)constructor\s*\[" ,

    # innerHTML sinks
    r"(?i)innerHTML\s*=",
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

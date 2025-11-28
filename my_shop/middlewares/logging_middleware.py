import time
from datetime import datetime
import re
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("unified")


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

class UnifiedSecurityMiddleware(MiddlewareMixin):

    def detect(self, text):
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
        try:
            request._body_data = (
                request.body.decode("utf-8", errors="ignore")
                if request.method in ("POST", "PUT", "PATCH")
                else None
            )
        except:
            request._body_data = None

    def process_response(self, request, response):
        if not hasattr(request, "_start_time"):
            return response

        duration = round((time.time() - request._start_time) * 1000, 2)

        full_path = request.get_full_path()
        query_params = request.META.get("QUERY_STRING", "")
        body = getattr(request, "_body_data", None)
        combined = f"{full_path} {query_params} {body or ''}"

        attack = self.detect(combined)

        log_data = {
            "event": "http_request",
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
                "username": str(request.user) if request.user.is_authenticated else None
            },

            "ip": request.headers.get("X-Forwarded-For") or request.META.get("REMOTE_ADDR"),
            "user_agent": request.headers.get("User-Agent"),

            "attack": attack,
            "type": "suspicious" if attack else "normal",
        }

        if attack:
            logger.warning("attack_detected", extra={"extra": log_data})
        else:
            logger.info("http_request", extra={"extra": log_data})

        return response
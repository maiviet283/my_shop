import os
from logging.handlers import TimedRotatingFileHandler
from datetime import timedelta, datetime
import logging
import json

class UnifiedDailyFileHandler(TimedRotatingFileHandler):
    def __init__(self, dirname, prefix):
        os.makedirs(dirname, exist_ok=True)
        filename = self._get_filename(dirname, prefix)
        super().__init__(filename, when="midnight", interval=1, backupCount=30, encoding="utf-8")
        self.dirname = dirname
        self.prefix = prefix

    def _get_filename(self, dirname, prefix):
        date = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(dirname, f"{prefix}-{date}.log")

    def doRollover(self):
        if self.stream:
            self.stream.close()
        self.baseFilename = self._get_filename(self.dirname, self.prefix)
        self.stream = self._open()


class AxesUnifiedHandler(logging.Handler):
    def emit(self, record):
        log = logging.getLogger("unified")
        log.info(
            "axes_event",
            extra={
                "extra": {
                    "event": "axes_event",
                    "type": "authentication",
                    "message": record.getMessage(),
                    "logger": "axes",
                }
            }
        )
        

class UnifiedJSONFormatter(logging.Formatter):

    DEFAULT_SCHEMA = {
        "timestamp": None,
        "level": None,
        "event": None,
        "logger": None,

        "method": None,
        "path": None,
        "full_path": None,
        "query_params": None,
        "body": None,

        "status_code": None,
        "duration_ms": None,
        "content_length": None,

        "user": {
            "authenticated": False,
            "username": None
        },

        "ip": None,
        "user_agent": None,
        "attack": None,
        "type": "normal",

        "message": None,
    }

    def format(self, record):
        data = {k: v for k, v in self.DEFAULT_SCHEMA.items()}
        vietnam_time = datetime.utcnow() + timedelta(hours=7)
        data["timestamp"] = vietnam_time.strftime("%Y-%m-%d %H:%M:%S")
        data["level"] = record.levelname
        data["logger"] = record.name

        # extra fields từ middleware / other logger
        extra = getattr(record, "extra", {})
        if isinstance(extra, dict):
            for k in data:
                if k in extra:
                    data[k] = extra[k]

        # fallback message
        msg = record.getMessage()
        if not data["event"]:
            data["event"] = msg
        data["message"] = msg

        return json.dumps(data, ensure_ascii=False)
    

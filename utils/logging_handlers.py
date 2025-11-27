import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

class IgnoreFaviconFilter(logging.Filter):
    def filter(self, record):
        msg = getattr(record, "msg", "")
        extra = getattr(record, "extra", {})
        path = extra.get("path") or ""
        return path != "/favicon.ico"

class DailyLogFileHandler(TimedRotatingFileHandler):

    def __init__(self, dirname, prefix, *args, **kwargs):
        self.dirname = dirname
        self.prefix = prefix
        os.makedirs(dirname, exist_ok=True)

        filename = self._get_filename()
        super().__init__(filename, when="midnight", interval=1, backupCount=30, encoding="utf-8")

    def _get_filename(self):
        date = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.dirname, f"{self.prefix}-{date}.log")

    def doRollover(self):
        if self.stream:
            self.stream.close()

        # Không rename file cũ → file theo ngày luôn đúng
        self.baseFilename = self._get_filename()
        self.stream = self._open()

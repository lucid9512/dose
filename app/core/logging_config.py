import logging
from logging.config import dictConfig
from app.core.config import settings
import os

LOG_PATH = os.path.join(settings.LOG_DIR, "app.log")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": settings.LOG_LEVEL,
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": LOG_PATH,
            "maxBytes": 10_485_760,
            "backupCount": 5,
            "level": settings.LOG_LEVEL,
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": settings.LOG_LEVEL,
    },
}

def setup_logging():
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    dictConfig(LOGGING_CONFIG)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

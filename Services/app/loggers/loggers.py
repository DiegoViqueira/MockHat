"""Loggers"""
import logging
import logging.config
from app.core.settings import settings


# Definir un diccionario de configuración de logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s|%(module)-10s|%(levelname)-8s|%(threadName)s|%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "access": {
            "format": "%(asctime)s|%(levelname)s|%(client_addr)s - '%(request_line)s' %(status_code)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
        },
        "access": {
            "formatter": "default",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {  # Logger raíz
            "handlers": ["default"],
            "level": settings.app.LOG_LEVEL,
            "propagate": True
        },
        "uvicorn": {"handlers": ["default"], "level": settings.app.LOG_LEVEL, "propagate": False},
        "uvicorn.error": {"handlers": ["default"], "level": settings.app.LOG_LEVEL, "propagate": False},
        "uvicorn.access": {"handlers": ["access"], "level": settings.app.LOG_LEVEL, "propagate": False},
    },
}


def set_logger():
    """Set the logger to the console."""

    log_level = settings.app.LOG_LEVEL or "ERROR"
    logging.config.dictConfig(LOGGING_CONFIG)
    # Forzar el mismo nivel a todos los handlers del root logger
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.setLevel(log_level)

    root_logger.info(
        "Logger configurado correctamente con nivel: %s", log_level)

"""Production settings for Travel Pro."""

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from decouple import config

from .base import *  # noqa: F403, F401

DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")], default="")

# ---------------------------------------------------------------------------
# Security hardening
# ---------------------------------------------------------------------------
SECURE_HSTS_SECONDS = 31_536_000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ---------------------------------------------------------------------------
# Admin URL (obscure in production)
# ---------------------------------------------------------------------------
ADMIN_URL = config("ADMIN_URL", default="secret-admin-xyz123/")

# ---------------------------------------------------------------------------
# Sentry
# ---------------------------------------------------------------------------
_sentry_dsn = config("SENTRY_DSN", default="")
if _sentry_dsn:
    sentry_sdk.init(
        dsn=_sentry_dsn,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment="production",
    )

# ---------------------------------------------------------------------------
# Cache: Redis
# ---------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL", default="redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
        "KEY_PREFIX": "travelpro",
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# ---------------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
import os as _os

_LOG_DIR = "/var/log/travelpro"
_file_handlers_available = _os.path.isdir(_LOG_DIR) and _os.access(_LOG_DIR, _os.W_OK)

_handlers = {
    "console": {
        "class": "logging.StreamHandler",
        "formatter": "verbose",
    },
}
_django_handlers = ["console"]
_dashboard_handlers = ["console"]

if _file_handlers_available:
    _handlers["file_error"] = {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": f"{_LOG_DIR}/error.log",
        "maxBytes": 10 * 1024 * 1024,
        "backupCount": 5,
        "formatter": "verbose",
        "level": "ERROR",
    }
    _handlers["file_dashboard"] = {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": f"{_LOG_DIR}/dashboard.log",
        "maxBytes": 5 * 1024 * 1024,
        "backupCount": 3,
        "formatter": "simple",
    }
    _django_handlers.append("file_error")
    _dashboard_handlers.append("file_dashboard")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {message}",
            "style": "{",
        },
    },
    "handlers": _handlers,
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": _django_handlers,
            "level": "WARNING",
            "propagate": False,
        },
        "dashboard": {
            "handlers": _dashboard_handlers,
            "level": "INFO",
            "propagate": False,
        },
    },
}

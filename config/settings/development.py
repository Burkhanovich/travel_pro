"""Development settings for Travel Pro."""

from .base import *  # noqa: F403, F401

DEBUG = True

INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE  # noqa: F405

INTERNAL_IPS = ["127.0.0.1", "localhost"]

# Use console email backend in development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Use local file storage in development instead of Cloudinary
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# Disable CSP in development for easier debugging
CSP_REPORT_ONLY = True  # noqa: F405

# Relaxed security for development
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Cache: use local-memory cache for development simplicity
# (override redis if redis not running locally)
CACHES = {  # noqa: F405
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Disable rate limiting in dev
RATELIMIT_ENABLE = False  # noqa: F405

# Debug toolbar config
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
    "SHOW_COLLAPSED": True,
}

# Exclude TemplatesPanel — it monkey-patches Template.render() adding ~10 frames
# per include, which exhausts the stack on complex pages with many nested templates.
DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

"""Test settings — fast, isolated, no debug toolbar / external services."""

from .base import *  # noqa: F403, F401

DEBUG = False

# Strip development-only tooling that interferes with template rendering and
# URL resolution during tests (debug toolbar registers a 'djdt' namespace only
# when DEBUG is on at request time).
INSTALLED_APPS = [a for a in INSTALLED_APPS if a != "debug_toolbar"]  # noqa: F405
MIDDLEWARE = [m for m in MIDDLEWARE if "debug_toolbar" not in m]  # noqa: F405

# Local-memory cache (no Redis needed).
CACHES = {  # noqa: F405
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
}

# Sessions in the DB so they don't depend on the cache backend.
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# No rate limiting during tests.
RATELIMIT_ENABLE = False

# Never hit the network for machine translation during tests.
AUTO_TRANSLATE = False

# In-memory email + local file storage.
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# Fast password hashing.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# In-memory SQLite for speed and isolation.
DATABASES = {  # noqa: F405
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

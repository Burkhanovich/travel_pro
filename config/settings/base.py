"""
Base Django settings for Travel Pro project.

All common settings shared between development and production.
Environment-specific overrides live in development.py / production.py.
"""

from pathlib import Path
from decouple import config, Csv
from django.utils.translation import gettext_lazy as _

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
SECRET_KEY: str = config("SECRET_KEY", default="django-insecure-dev-only-change-in-production-abc123xyz")
ALLOWED_HOSTS: list[str] = config("ALLOWED_HOSTS", cast=Csv(), default="localhost,127.0.0.1")

# ---------------------------------------------------------------------------
# Application definition
# ---------------------------------------------------------------------------
DJANGO_APPS = [
    # modeltranslation MUST precede django.contrib.admin
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.humanize",
]

THIRD_PARTY_APPS = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rosetta",
    "django_filters",
    "crispy_forms",
    "crispy_tailwind",
    "ckeditor",
    "ckeditor_uploader",
    "cloudinary_storage",
    "cloudinary",
    "whitenoise.runserver_nostatic",
    "django_celery_results",
    "django_celery_beat",
    "import_export",
]

LOCAL_APPS = [
    "apps.core",
    "apps.tours",
    "apps.destinations",
    "apps.hotels",
    "apps.bookings",
    "apps.mice",
    "apps.guides",
    "apps.reviews",
    "apps.accounts",
    "apps.dashboard",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "csp.middleware.CSPMiddleware",
    "apps.dashboard.middleware.DashboardAccessMiddleware",
]

# ── Dashboard / Admin security ────────────────────────────────────────────────
ADMIN_URL = "secret-admin-xyz123/"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 3600 * 8  # 8 hours

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "apps.core.context_processors.site_settings",
                "apps.core.context_processors.navigation",
                "apps.core.context_processors.languages",
                "apps.dashboard.context_processors.dashboard_counts",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ---------------------------------------------------------------------------
# Database (configured per environment)
# ---------------------------------------------------------------------------
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL", default="sqlite:///db.sqlite3"),
        conn_max_age=600,
    )
}

# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_USER_MODEL = "auth.User"
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = config("LANGUAGE_CODE", default="en")

LANGUAGES = [
    ("en", _("English")),
    ("uz", _("O'zbekcha")),
    ("ru", _("Русский")),
    ("it", _("Italiano")),
    ("es", _("Español")),
    ("ja", _("日本語")),
]

LANGUAGE_FLAGS = {
    "en": "🇬🇧",
    "uz": "🇺🇿",
    "ru": "🇷🇺",
    "it": "🇮🇹",
    "es": "🇪🇸",
    "ja": "🇯🇵",
}

TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "locale"]

# ---------------------------------------------------------------------------
# Static & Media files
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Cloudinary
import cloudinary

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME", default=""),
    "API_KEY": config("CLOUDINARY_API_KEY", default=""),
    "API_SECRET": config("CLOUDINARY_API_SECRET", default=""),
}
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# ---------------------------------------------------------------------------
# Default primary key
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Sites framework
# ---------------------------------------------------------------------------
SITE_ID = 1

# ---------------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="Travel Pro <noreply@travelpro.com>")

# ---------------------------------------------------------------------------
# Celery
# ---------------------------------------------------------------------------
CELERY_BROKER_URL = config("REDIS_URL", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# ---------------------------------------------------------------------------
# Cache (Redis)
# ---------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL", default="redis://localhost:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# ---------------------------------------------------------------------------
# django-allauth
# ---------------------------------------------------------------------------
# django-allauth v65+ settings
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# ---------------------------------------------------------------------------
# CKEditor
# ---------------------------------------------------------------------------
CKEDITOR_UPLOAD_PATH = "ckeditor_uploads/"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Bold", "Italic", "Underline"],
            ["NumberedList", "BulletedList", "-", "Outdent", "Indent"],
            ["JustifyLeft", "JustifyCenter", "JustifyRight"],
            ["Link", "Unlink"],
            ["RemoveFormat", "Source"],
            ["Image", "Table", "HorizontalRule"],
            ["Styles", "Format"],
        ],
        "height": 400,
        "width": "100%",
        "removePlugins": "elementspath",
        "resize_enabled": True,
        "extraPlugins": "image2",
    }
}

# ---------------------------------------------------------------------------
# Crispy Forms
# ---------------------------------------------------------------------------
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

# ---------------------------------------------------------------------------
# django-modeltranslation
# ---------------------------------------------------------------------------
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
MODELTRANSLATION_LANGUAGES = ("en", "uz", "ru", "it", "es", "ja")
MODELTRANSLATION_FALLBACK_LANGUAGES = ("en",)

# ---------------------------------------------------------------------------
# Rate limiting (django-ratelimit) — module is django_ratelimit
# ---------------------------------------------------------------------------
RATELIMIT_USE_CACHE = "default"
RATELIMIT_ENABLE = True

# ---------------------------------------------------------------------------
# CSP headers (django-csp)
# ---------------------------------------------------------------------------
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    "fonts.googleapis.com",
    "cdn.jsdelivr.net",
    "unpkg.com",
)
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    "cdn.jsdelivr.net",
    "unpkg.com",
    "cdnjs.cloudflare.com",
)
CSP_FONT_SRC = ("'self'", "fonts.gstatic.com", "fonts.googleapis.com")
CSP_IMG_SRC = ("'self'", "data:", "res.cloudinary.com", "*.tile.openstreetmap.org")
CSP_CONNECT_SRC = ("'self'",)

# ---------------------------------------------------------------------------
# Site meta (used by context processor)
# ---------------------------------------------------------------------------
SITE_NAME = config("SITE_NAME", default="Travel Pro")
SITE_URL = config("SITE_URL", default="http://localhost:8000")
SITE_TAGLINE = "Discover the World with Confidence"
SITE_PHONE = "+1 (555) 123-4567"
SITE_EMAIL = "info@travelpro.com"
SITE_ADDRESS = "123 Travel Street, New York, NY 10001"
SOCIAL_LINKS = {
    "facebook": "https://facebook.com/travelpro",
    "instagram": "https://instagram.com/travelpro",
    "twitter": "https://twitter.com/travelpro",
    "youtube": "https://youtube.com/travelpro",
    "telegram": "https://t.me/travelpro",
}

# ---------------------------------------------------------------------------
# django-import-export
# ---------------------------------------------------------------------------
IMPORT_EXPORT_USE_TRANSACTIONS = True

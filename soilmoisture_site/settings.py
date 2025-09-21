from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security / Debug ---
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key-change-in-prod")
DEBUG = os.getenv("DJANGO_DEBUG", "true").lower() == "true"

# Comma-separated list, default allow all for ease; restrict in production
ALLOWED_HOSTS = [h for h in os.getenv("ALLOWED_HOSTS", "*").split(",") if h]
_raw_csrf = os.getenv("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _raw_csrf.split(",") if o.strip()]

# --- Apps ---
INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "core",
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise for static files on Render
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",  # important for HTMX posts
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "soilmoisture_site.urls"

# --- Templates ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [ BASE_DIR / "core" / "templates" ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "soilmoisture_site.wsgi.application"

# --- Database ---
# Use DATABASE_URL if present (e.g., Render PostgreSQL), else fall back to SQLite.
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://"),
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --- Internationalization / TZ ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Toronto"
USE_I18N = True
USE_TZ = True

# --- Static files ---
STATIC_URL = "static/"
STATICFILES_DIRS = [ BASE_DIR / "core" / "static" ]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Django 5 storage with WhiteNoise hashed files
STORAGES = {
    "default": { "BACKEND": "django.core.files.storage.FileSystemStorage" },
    "staticfiles": { "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage" },
}

# When behind Render’s proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

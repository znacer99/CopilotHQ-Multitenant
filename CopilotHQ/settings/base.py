import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = "replace-this-later"
DEBUG = True

ALLOWED_HOSTS = ["*"]

# =====================================
# DJANGO TENANTS APP CONFIG
# =====================================

# Extra search paths so django-tenants always finds the public schema first
PG_EXTRA_SEARCH_PATHS = []

SHARED_APPS = [
    "django_tenants",          # must be first
    "tenants",                 # public schema, stores Client + Domain

    # Django core apps (all must be in public)
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # accounts MUST be public (superadmin lives here)
    "accounts",
]

TENANT_APPS = [
    "rest_framework",

    # tenant-only apps (each company has its own copy)
    "employees",
    "departments",
    "documents",
    "leave",
    "candidates",
    "dashboard",
    "api",
    "common",
]

INSTALLED_APPS = SHARED_APPS + TENANT_APPS

TENANT_MODEL = "tenants.Client"
TENANT_DOMAIN_MODEL = "tenants.Domain"

DATABASE_ROUTERS = (
    "django_tenants.routers.TenantSyncRouter",
)

DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": os.environ.get("POSTGRES_DB", "copilotdb"),
        "USER": os.environ.get("POSTGRES_USER", "copilot"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "copilotpw"),
        "HOST": os.environ.get("POSTGRES_HOST", "postgres"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 0,
        "OPTIONS": {
            "options": "-c search_path=public"
        },
    }
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django_tenants.middleware.main.TenantMainMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "CopilotHQ.urls_tenant"
PUBLIC_SCHEMA_URLCONF = "CopilotHQ.urls_public"
TENANT_BASE_URLCONF = "CopilotHQ.urls_tenant"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

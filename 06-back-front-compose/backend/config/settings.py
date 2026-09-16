import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-not-for-production",
)

DEBUG = True

# El hostname del contenedor (untdf-api) y localhost si publicás el puerto.
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "ciudades",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# HOST tiene que ser el *nombre del contenedor* de Postgres en la red Docker.
# Desde el navegador de tu máquina ese nombre no existe.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "ciudades"),
        "USER": os.environ.get("POSTGRES_USER", "untdf"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "untdf"),
        "HOST": os.environ.get("POSTGRES_HOST", "untdf-db"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Ushuaia"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# visitas_medicas/settings.py
from pathlib import Path
from django.contrib.messages import constants as messages
import os
import sys  # ¡AGREGAR ESTA LÍNEA!
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# Seguridad / Entorno
# =========================
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-unsafe-key")

# 🔥 FORZAMOS DEBUG EN LOCAL
DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "visitasmedicasdiphasac-production.up.railway.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://visitasmedicasdiphasac-production.up.railway.app",
]

# Desactivar config de proxy para dev si causa conflicto (opcional)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# =========================
# Cookies para DESARROLLO (http)
# =========================
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = False      # ❗ en local debe ser False
SESSION_COOKIE_SECURE = False   # ❗ en local debe ser False
CSRF_COOKIE_HTTPONLY = False

# Vista de error CSRF
CSRF_FAILURE_VIEW = "apps.usuarios.views.csrf_failure"

# =========================
# Django apps
# =========================
AUTH_USER_MODEL = "usuarios.Usuario"
LOGIN_REDIRECT_URL = "inicio"
LOGOUT_REDIRECT_URL = "/"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.usuarios",
    "apps.doctores",
    "apps.asistencia",
    "apps.productos",
    "apps.rutas",
    "apps.visitas",
    "apps.ubicaciones",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.usuarios.middlewares.PasswordChangeMiddleware",
]

ROOT_URLCONF = "visitas_medicas.urls"

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

WSGI_APPLICATION = "visitas_medicas.wsgi.application"

# =========================
# Base de datos (local SQLite)
# =========================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# =========================
# Password validators
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =========================
# Localización
# =========================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/Lima"
USE_TZ = True
USE_I18N = True
USE_L10N = True

# =========================
# Estáticos / WhiteNoise
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MESSAGE_TAGS = {
    messages.DEBUG: "secondary",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}
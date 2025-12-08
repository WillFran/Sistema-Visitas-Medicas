# test_settings.py (en la misma carpeta que settings.py)
from .settings import *

print("\n" + "="*60)
print("⚡ USANDO CONFIGURACIÓN ESPECIAL PARA TESTING")
print("="*60)

# ============================================
# SOBREESCRIBIR CONFIGURACIONES PARA TESTING
# ============================================

# 1. FORZAR DEBUG TRUE
DEBUG = True
TEMPLATE_DEBUG = True
print("✅ DEBUG forzado a True")

# 2. DESACTIVAR CSRF COMPLETAMENTE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ⚠️ CSRF DESACTIVADO - NO ESTÁ EN LA LISTA
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.usuarios.middlewares.PasswordChangeMiddleware',
]
print("✅ Middleware configurado SIN CSRF")

# 3. CONFIGURACIÓN EXTREMA DE CSRF
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_DOMAIN = None
CSRF_TRUSTED_ORIGINS = []
print("✅ Configuración CSRF desactivada")

# 4. BASE DE DATOS EN MEMORIA
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
print("✅ Base de datos en memoria configurada")

# 5. DESACTIVAR WHITENOISE PARA TESTING
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# 6. LOGGING DETALLADO
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'apps.rutas': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
print("✅ Logging configurado")

print("="*60 + "\n")
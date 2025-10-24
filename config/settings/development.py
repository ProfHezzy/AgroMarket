"""
Development settings for AgroMarket project.
"""
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database - Using SQLite for quick setup
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Uncomment below for PostgreSQL setup
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': env('DB_NAME', default='agromarket_dev'),
#         'USER': env('DB_USER', default='postgres'),
#         'PASSWORD': env('DB_PASSWORD', default='password'),
#         'HOST': env('DB_HOST', default='localhost'),
#         'PORT': env('DB_PORT', default='5432'),
#     }
# }

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

# Django Debug Toolbar (optional)
if DEBUG:
    INSTALLED_APPS += ['django_extensions']
    
# Override Redis settings for development - use database instead
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

# Use database sessions instead of Redis
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
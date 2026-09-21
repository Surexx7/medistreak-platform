"""
Django settings for MediScope project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

# Load environment variables from .env
load_dotenv(BASE_DIR / '.env')


# ============================================================
# SECURITY
# ============================================================

# Keep this value inside your .env file.
SECRET_KEY = os.environ['SECRET_KEY']

# DEBUG=True for local development.
# DEBUG=False for production.
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'


# Example .env:
# ALLOWED_HOSTS=127.0.0.1,localhost
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv('ALLOWED_HOSTS', '').split(',')
    if host.strip()
]


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    # Third-party apps
    'jazzmin',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party packages
    'corsheaders',

    # MediScope apps
    'core',
    'cases',
    'quizzes',
    'anatomy',
    'ai_checker',
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise should come directly after SecurityMiddleware.
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    # CORS middleware
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================
# URL / WSGI CONFIGURATION
# ============================================================

ROOT_URLCONF = 'mediscope.urls'

WSGI_APPLICATION = 'mediscope.wsgi.application'


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates',
        ],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # AI Checker notifications
                'ai_checker.context_processors.notification_count',
            ],
        },
    },
]


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Production / PostgreSQL
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }
else:
    # Local development / SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.'
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.'
        'MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.'
        'CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.'
        'NumericPasswordValidator',
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

# Browser URL for static files.
STATIC_URL = '/static/'

# Development static directory.
#
# Project structure:
#
# mediscope-platform/
# ├── static/
# ├── staticfiles/
# ├── media/
# └── manage.py
#
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# IMPORTANT:
# WhiteNoise and collectstatic need this directory.
#
# This was the cause of the:
#
# "You're using the staticfiles app without having set
# the STATIC_ROOT setting"
#
# error.
STATIC_ROOT = BASE_DIR / 'staticfiles'


# ============================================================
# STORAGE CONFIGURATION
# ============================================================

STORAGES = {

    # --------------------------------------------------------
    # Uploaded files
    # --------------------------------------------------------
    #
    # Used by:
    #
    # question.image
    # profile images
    # uploaded media
    # etc.
    #
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },

    # --------------------------------------------------------
    # Static files
    # --------------------------------------------------------
    #
    # Used for:
    #
    # CSS
    # JavaScript
    # icons
    # anatomy thumbnails
    # static images
    #
    "staticfiles": {
        "BACKEND":
        "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ============================================================
# MEDIA / USER UPLOADS
# ============================================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================
# AUTHENTICATION
# ============================================================

LOGIN_URL = '/auth/login/'

LOGIN_REDIRECT_URL = '/dashboard/'

LOGOUT_REDIRECT_URL = 'home'


# ============================================================
# CORS
# ============================================================

# Example .env:
#
# CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        'CORS_ALLOWED_ORIGINS',
        ''
    ).split(',')
    if origin.strip()
]

# During local development, allow all origins only when
# no explicit CORS_ALLOWED_ORIGINS have been configured.
CORS_ALLOW_ALL_ORIGINS = (
    DEBUG and not CORS_ALLOWED_ORIGINS
)


# ============================================================
# GEMINI API
# ============================================================

# Put your Gemini API key inside .env:
#
# GEMINI_API_KEY=your-api-key
#
# Never hardcode the real API key here.

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


# ============================================================
# PRODUCTION SECURITY
# ============================================================

if not DEBUG:

    SECURE_PROXY_SSL_HEADER = (
        'HTTP_X_FORWARDED_PROTO',
        'https',
    )

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    CSRF_TRUSTED_ORIGINS = [
        f'https://{host}'
        for host in ALLOWED_HOSTS
        if host
    ]


# ============================================================
# JAZZMIN ADMIN CONFIGURATION
# ============================================================

JAZZMIN_SETTINGS = {

    "site_title": "MediStreak Admin",

    "site_header": "MediStreak Dashboard",

    "site_brand": "MediStreak",

    "welcome_sign": "Welcome to MediStreak Admin",

    "copyright": "MediStreak",

    "show_sidebar": True,

    "navigation_expanded": True,

    "icons": {
        "auth": "fas fa-users-cog",
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
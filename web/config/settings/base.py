import os
from datetime import timedelta
from pathlib import Path


import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = os.path.abspath(os.path.join(__file__, "../../../.."))
APPS_DIR = os.path.join(ROOT_DIR, "web")

# Only for local development and CI, env variables take precedence
env = environ.Env()
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)

if READ_DOT_ENV_FILE:
    env.read_env(os.path.join(ROOT_DIR, ".env"))

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = []

# Application definition
DJANGO_APPS = [
    "material",
    "material.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_api_key",
    "rest_framework_simplejwt",
    "corsheaders",
    "imagekit",
    "phonenumber_field",
    "anymail",
    "django_extensions",
    "django_json_widget",
    "tinymce",
]

LOCAL_APPS = [
    "web.apps.base",
    "web.apps.users",
    "web.apps.vendors",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "web.config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "web.config.wsgi.application"
ASGI_APPLICATION = "web.config.asgi.application"


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
AUTH_USER_MODEL = "users.User"

LANGUAGE_CODE = "es-co"

TIME_ZONE = "America/Bogota"

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # Formatters ###########################################################
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
    },
    # Handlers #############################################################
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "verbose"}},
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    # Loggers ###############################################################
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "django": {
            "propagate": True,
        },
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Media files
MEDIAFILES_LOCATION = "media"
MEDIA_URL = "/media/"

# Redis
REDIS_PASSWORD = env.str("REDIS_PASSWORD", "")
REDIS_HOST = env.str("REDIS_HOST")
REDIS_PORT = env.str("REDIS_PORT", "6379")

REDIS_URL_PRE = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_URL_PRE}/0",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": None,
    }
}

# Sessions con redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# CONFIGURACIÓN DJANGO-REST-FRAMEWORK
API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "web.utils.renderers.webRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework_api_key.permissions.HasAPIKey",
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "EXCEPTION_HANDLER": "web.utils.handlers.web_api_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "web.apps.base.utils.StandardResultsPagination",
}

# CONFIGURACIÓN DEL TOKEN
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=12),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=12),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "uuid",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(hours=12),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(hours=12),
}

# Config Admin Material
MATERIAL_ADMIN_SITE = {
    "HEADER": "Dashboard",
    "TITLE": "dashboard admin",
    "FAVICON": "path/to/favicon",  # Admin site favicon (path to static should be specified)
    "MAIN_BG_COLOR": "#004d7e",
    "MAIN_HOVER_COLOR": "#004d7e",
    "SHOW_COUNTS": True,
    "APP_ICONS": {
        "users": "person",
        "rest_framework_api_key": "lock",
        "django_celery_beat": "history",
    },
}

NUMBER_PAGINATION_ADMIN = 10

CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ORIGIN_ALLOW_ALL", True)
PHONENUMBER_DEFAULT_REGION = "CO"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# TWILIO SMS
TWILIO_ACCOUNT_SID = env.str("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env.str("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_SENDER = env.str("TWILIO_PHONE_SENDER")

# INFO AUTO
INFO_AUTO_USER = env.str("INFO_AUTO_USER")
INFO_AUTO_PASSWORD = env.str("INFO_AUTO_PASSWORD")
INFO_AUTO_URL_BASE = env.str("INFO_AUTO_URL_BASE")

# SENDGRID
SENDGRID_API_KEY = env.str("SENDGRID_API_KEY")

# Config Mail
EMAIL_SUBJECT_PREFIX = "Dashboard "
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = "Dashboard <contact@lsv.com>"
SERVER_EMAIL = "tech@lsv.com"  # default from-email for Django errors

ANYMAIL = {
    "SENDGRID_API_KEY": SENDGRID_API_KEY,
}

# SENTRY
SENTRY_DSN_KEY = env.str("SENTRY_DSN_KEY")

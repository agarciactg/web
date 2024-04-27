import os

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from corsheaders.defaults import default_headers

from web.config.settings.base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    "X-Api-Key",
]

ALLOWED_HOSTS = ["*"]

# Static files
STATIC_ROOT = os.path.join(ROOT_DIR, "static")  # noqa
# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # noqa


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": os.environ["POSTGRES_PORT"],
    }
}

MIDDLEWARE += [  # noqa
    "corsheaders.middleware.CorsMiddleware",
    "corsheaders.middleware.CorsPostCsrfMiddleware",
]

sentry_sdk.init(
    dsn=SENTRY_DSN_KEY,
    integrations=[DjangoIntegration(), RedisIntegration(), CeleryIntegration()],
    send_default_pii=True,
)

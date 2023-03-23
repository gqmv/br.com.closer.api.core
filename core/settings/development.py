"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from base import *

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_USE_SESSIONS = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_DOMAIN = "closer-api-core-htnicielra-uc.a.run.app"
SECURE_BROWSER_XSS_FILTER = True
SESSION_ENGINE = "django.contrib.sessions.backends.db"

if os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # Use django-environ to parse DATABASE_URL from secrets
    DATABASES = {"default": env.db()}


# If using Cloud SQL Auth Proxy, change the database values accordingly.
if os.environ.get("USE_CLOUD_SQL_AUTH_PROXY"):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432


# Define static storage via django-storages[google]
if env.get_value("GS_BUCKET_NAME", default=None):
    GS_BUCKET_NAME = env("GS_BUCKET_NAME")
    STATICFILES_DIRS = []
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_DEFAULT_ACL = "publicRead"


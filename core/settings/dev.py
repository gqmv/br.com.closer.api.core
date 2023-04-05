import io
import os
from urllib.parse import urlparse
from google.cloud import secretmanager, logging
import google.auth

import environ

# Import the original settings from each template
from .base import *

# Load the settings from the secret manager
env = environ.Env()
_, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
client = secretmanager.SecretManagerServiceClient()
settings_name = "application_settings"
name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

env.read_env(io.StringIO(payload))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

GOOGLE_FUNCTION_SERVICE_ACCOUNT = env("GOOGLE_FUNCTION_SERVICE_ACCOUNT")

# SSL settings
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
CSRF_USE_SESSIONS = False

# Security settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_ENGINE = "django.contrib.sessions.backends.db"


# SECURITY WARNING: define the correct hosts in production!
# CSRF Settings
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
    SESSION_COOKIE_DOMAIN = urlparse(CLOUDRUN_SERVICE_URL).netloc
else:
    ALLOWED_HOSTS = ["*"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=False)

# In production, we use Cloud SQL
DATABASES = {"default": env.db()}

# Change database settings if using the Cloud SQL Auth Proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432


# Define static storage via django-storages[google]
GS_BUCKET_NAME = env("GS_BUCKET_NAME")
STATICFILES_DIRS = []
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = "publicRead"

# WhatsApp settings
WHATSAPP_TOKEN = env("WHATSAPP_TOKEN")
WHATSAPP_NUMBER_ID = env("WHATSAPP_NUMBER_ID")

client = logging.Client()
handler = client.setup_logging()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "gcp": {
            "class": "google.cloud.logging.handlers.CloudLoggingHandler",
            "client": client,
        },
    },
    "loggers": {
        "": {
            "handlers": ["gcp"],
            "level": "INFO",
        },
    },
}

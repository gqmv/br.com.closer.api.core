import io
import os
from urllib.parse import urlparse
from google.cloud import secretmanager
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

# If defined, add service URL to Django security settings
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
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

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "local-secret-key"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

# In local development, we use sqlite3
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# WhatsApp settings
WHATSAPP_TOKEN = None
WHATSAPP_NUMBER_ID = None

GOOGLE_FUNCTION_SERVICE_ACCOUNT = "test-service-account"

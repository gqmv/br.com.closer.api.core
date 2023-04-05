from .base import *
from google.cloud import logging_v2


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


try:
    logging_client = logging_v2.Client()
    handler = logging_client.setup_logging()

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "gcp": {
                "class": "google.cloud.logging_v2.handlers.CloudLoggingHandler",
                "client": logging_client,
            },
        },
        "loggers": {
            "": {
                "handlers": ["gcp"],
                "level": "INFO",
            },
            "root": {
                "handlers": ["gcp"],
                "level": "INFO",
            },
            "django": {
                "handlers": ["gcp"],
                "level": "INFO",
            },
            "django.request": {
                "handlers": ["gcp"],
                "level": "INFO",
            },
        },
    }
except:
    pass

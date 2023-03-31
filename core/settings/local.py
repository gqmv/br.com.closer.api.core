from .base import *

# Load the settings from the environment variable
env = environ.Env()
env.read_env()

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
WHATSAPP_TOKEN = env("WHATSAPP_TOKEN", default=None)
WHATSAPP_NUMBER_ID = env("WHATSAPP_NUMBER_ID", default=None)

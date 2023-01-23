from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "u-a$@li2^iel7c31e6-zdb4!yz9utm3i+#00)*=7%55cgm6jic"


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

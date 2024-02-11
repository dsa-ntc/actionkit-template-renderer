import contextlib
import os
from pathlib import Path

DEBUG = True
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "mydsa.apps.MyDsaConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "dsa_actionkit.urls"

WSGI_APPLICATION = "dsa_actionkit.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite",
    },
    # "roboticdogs": {
    #     "ENGINE": "django.db.backends.mysql",
    #     "NAME": "ak_roboticdogs",
    #     "USER": os.getenv("ROBOTIC_DOGS_USER"),
    #     "PASSWORD": os.getenv("ROBOTIC_DOGS_PASSWORD"),
    #     "HOST": "roboticdogs.client-db.actionkit.com",
    # },
}


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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

APP_PATH = Path().parent
PROJECT_ROOT_PATH = Path.resolve(Path.cwd())

STATIC_ROOT = os.environ.get("STATIC_ROOT", PROJECT_ROOT_PATH / "static")
STATIC_URL = os.environ.get("STATIC_URL", "/static/")
STATIC_FALLBACK = os.environ.get("STATIC_FALLBACK", False)
STATIC_LOCAL = os.environ.get("STATIC_URL", None)
DEFAULT_TEMPLATES = APP_PATH / "templates"
DIR_TEMPLATES = []
if os.environ.get("TEMPLATE_DIR"):
    DIR_TEMPLATES.append(os.environ.get("TEMPLATE_DIR"))
else:
    for d in ("template_set/", "_layouts/", "_includes/"):
        dd = PROJECT_ROOT_PATH / d
        if Path.exists(dd):
            DIR_TEMPLATES.append(dd)

DIR_TEMPLATES.append(DEFAULT_TEMPLATES)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": DIR_TEMPLATES,
        "APP_DIRS": True,
        "OPTIONS": {
            "builtins": ["dsa_actionkit.templatetags.actionkit_tags"],
        },
    },
]

MIDDLEWARE_CLASSES = []


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite",
    },
}

"""
Django settings for the transcribee-backend project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

from configurations import Configuration, values

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Base(Configuration):
    AUTH_USER_MODEL = "base.User"

    SECRET_KEY = values.Value()
    DEBUG = values.Value()

    ALLOWED_HOSTS = values.ListValue(["*"])

    # Application definition

    INSTALLED_APPS = [
        "daphne",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "rest_framework",
        "rest_framework.authtoken",
        "transcribee_backend.base",
        "transcribee_backend.api",
        "transcribee_backend.sync",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "transcribee_backend.base.middleware.WorkerTokenMiddleware",
    ]

    ROOT_URLCONF = "transcribee_backend.urls"

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

    WSGI_APPLICATION = "transcribee_backend.wsgi.application"

    # Password validation
    # https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
    # https://docs.djangoproject.com/en/4.1/topics/i18n/

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = "UTC"

    USE_I18N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.1/howto/static-files/

    STATIC_URL = "static/"

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

    LOGIN_URL = "login"

    STATIC_ROOT = BASE_DIR / "static"

    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.TokenAuthentication",
            "rest_framework.authentication.BasicAuthentication",
            "rest_framework.authentication.SessionAuthentication",
        ]
    }

    ASGI_APPLICATION = "transcribee_backend.asgi.application"

    TRANSCRIBEE_WORKER_TIMEOUT = 10 * 60  # Timeout in seconds, 10 Minutes
    # Time in milliseconds to wait after every message of the initial editor sync
    TRANSCRIBEE_INITIAL_SYNC_SLOWDOWN = 0

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv("DKEY")


# ! Switch to False when in production
DEBUG = True

# Todo: Add web url when in production
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "web-production-a9ad9.up.railway.app", "track-it-wfy4.onrender.com"]

# fmt: off
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'home.apps.HomeConfig',
    'users.apps.UsersConfig',
    'administrator.apps.AdministratorConfig',
    'adviser.apps.AdviserConfig',
    'helpers',
    'storages',
    'widget_tweaks',
]
# fmt: on


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ! Comment out this when in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "capstoneMonitoringSystem.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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


WSGI_APPLICATION = "capstoneMonitoringSystem.wsgi.application"


# ! Configure when in production
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# * Railway Online DB
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_RAILWAY_NAME"),
        "USER": os.getenv("DB_RAILWAY_USER"),
        "PASSWORD": os.getenv("DB_RAILWAY_PASSWORD"),
        "HOST": os.getenv("DB_RAILWAY_HOST"),
        "PORT": os.getenv("DB_RAILWAY_PORT"),
    }
}


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


LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Manila"
USE_I18N = True
USE_TZ = True


STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
AUTH_USER_MODEL = "users.User"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "testdjangomail1@gmail.com"
EMAIL_HOST_PASSWORD = "glbvevmaceekrywn"


# ? Comment this out when in local
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE")
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

# ! Configure this for later
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ! Configure this for later
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8080",
    "https://web-production-a9ad9.up.railway.app",
    "https://track-it-wfy4.onrender.com"
]


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

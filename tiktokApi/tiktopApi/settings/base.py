import os
from pathlib import Path
from .prod import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print('what is basedir >>>>>>>>>>------->>>> ', BASE_DIR)

# Application definition
INSTALLED_APPS = [
    # channels
    "channels",
    # django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # internal apps
    "apps.core",
    "apps.postsapi",
    # "api",
    "apps.accounts",
    "apps.like",
    "apps.comments",
    "apps.search",
    #  do i need to use this as a separate app? or not think it later.
    "common.pagination",
    "notifications",
    # third party apps
    "drf_spectacular",
    # external apps
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "whitenoise.middleware.WhiteNoiseMiddleware", # for production static files
    # corse header
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tiktopApi.urls"

WSGI_APPLICATION = "tiktopApi.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Add your templates directory here
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


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# In settings.py
# AUTH_USER_MODEL = 'api.User'  # Ensure 'api' is the app where the User model is defined


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = "static/"
# For production builds only
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# For redirections, it is django default behaviour
APPEND_SLASH = False

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# AUTH_USER_MODEL = "api.User"  # 'api' should be the name of your app
AUTH_USER_MODEL = (
    "accounts.User"  # "accounts.User"  # 'accounts' should be the name of your app
)


# Allow headers and methods if needed:
# CORS_ALLOW_HEADERS = ['*']
# CORS_ALLOW_METHODS = ['GET', 'POST', 'OPTIONS']

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Allow credentials (e.g., cookies, Authorization headers)
CORS_ALLOW_CREDENTIALS = True


# Optional: Allow all HTTP methods
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        # "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": "10/hour",  # Customize rate limits
        "anon": "10/minute",
    },
}


# Step 1: Configure Django to Use File-Based Caching
# Add the following configuration to your settings.py file to enable file-based caching in a dedicated folder:

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, "cache"),  # Cache directory
        "TIMEOUT": 30000,  # Default timeout for cache (in seconds)
        "OPTIONS": {
            "MAX_ENTRIES": 10000,  # Maximum number of cache entries
            "CULL_FREQUENCY": 3,  # Cull a third of entries when limit is hit
        },
    }
}

# drf specatacular
# Step 2: Configure Django REST Framework to Use Spectacular for OpenAPI Schema Generation
# Add the following configuration to your settings.py file to enable Spectacular for OpenAPI schema generation:
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


# CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

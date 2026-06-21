import os

from dotenv import load_dotenv

from .base import *
# from .base import BASE_DIR
# from settings.base import BASE_DIR

load_dotenv()

DEBUG = True

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-dev-key")

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent / "database" / "db.sqlite3",
    }
}

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# # settings/dev.py


# import os
# from .base import *  # ✅ OK — prod can import base, not the other way

# from dotenv import load_dotenv

# load_dotenv()

# DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

# ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")
# SECRET_KEY = os.environ.get("SECRET_KEY")

# # """
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR.parent / "database" / "db.sqlite3",  # noqa: F405
#     }
# }

# # print("on dev file ", BASE_DIR.parent)
# # """


# # Database WITH PostgreSQL
# # https://docs.djangoproject.com/en/5.0/ref/settings/#databases
# # DATABASES = {
# #     "default": {
# #         "ENGINE": "django.db.backends.postgresql",
# #         "NAME": "tiktokapi",  # database name
# #         "USER": "admin",
# #         "PASSWORD": "admin",
# #         "HOST": "localhost",
# #         "PORT": "5432",
# #     }
# # }

# # CSRF_TRUSTED_ORIGINS = [
# #     "http://localhost:3000",  # Frontend origin
# #     "http://127.0.0.1:3000",  # Frontend origin
# # ]

# # CORS_ALLOWED_ORIGINS = [
# #     "http://localhost:3000",  # Add your frontend's URL
# #     "http://127.0.0.1:3000",  # If you're using localhost
# # ]


# # CSRF_COOKIE_SAMESITE = "Lax"
# # SESSION_COOKIE_SAMESITE = "Lax"
# # CSRF_COOKIE_SECURE = False
# # SESSION_COOKIE_SECURE = False

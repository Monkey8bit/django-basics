from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("django_shop_secret")
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get("github_shop_secret")
SOCIAL_AUTH_GITHUB_KEY = os.environ.get("github_shop_client")
SOCIAL_AUTH_VK_OAUTH2_KEY = os.environ.get("vk_shop_id")
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.environ.get("vk_shop_secret")
DJANGO_PRODUCTION = bool(os.environ.get("django_shop_prod", False))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "185.46.11.155"]

INTERNAL_IPS = [
    "127.0.0.1"
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "template_profiler_panel",
    "social_django",
    "mainapp",
    "authapp",
    "cartapp",
    "adminapp",
    "ordersapp",
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.history.HistoryPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]


def show_toolbar(request):
    return bool(request.GET.get("debug"))


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}


MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "shop.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "mainapp.context_processors.menu",
            ],
        },
    },
]

WSGI_APPLICATION = "shop.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


if DJANGO_PRODUCTION:
    DJANGO_DB_NAME = os.environ.get("django_db_name")
    DJANGO_DB_USER = os.environ.get("django_db_user")
    DJANGO_DB_PASSWORD = os.environ.get("django_db_password")
    DJANGO_DB_HOST = os.environ.get("django_db_host")
    DJANGO_DB_PORT = int(os.environ.get("django_db_port"))

    # assert all([
    #     DJANGO_DB_NAME,
    #     DJANGO_DB_USER,
    #     DJANGO_DB_PASSWORD,
    #     DJANGO_DB_HOST,
    #     DJANGO_DB_PORT
    # ])

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": DJANGO_DB_NAME,
            "USER": DJANGO_DB_USER,
            "PASSWORD": DJANGO_DB_PASSWORD,
            "HOST": DJANGO_DB_HOST,
            "PORT": DJANGO_DB_PORT,
            "OPTIONS": {
                'client_encoding': 'LATIN1',
            }
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": ("django.contrib.auth.password_validation" ".UserAttributeSimilarityValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.MinimumLengthValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.NumericPasswordValidator"),
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

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Auth
AUTH_USER_MODEL = "authapp.ShopUser"
LOGIN_URL = "/auth/login"
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "social_core.backends.github.GithubOAuth2",
    "social_core.backends.vk.VKOAuth2",
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = "indexs"

# SOCIAL_AUTH_PIPELINE = (
#     "social_core.pipeline.social_auth.social_details",
#     "social_core.pipeline.social_auth.social_uid",
#     "social_core.pipeline.social_auth.auth_allowed",
#     "social_core.pipeline.social_auth.social_user",
#     "social_core.pipeline.user.create_user",
#     "authapp.pipeline.save_user_profile",
#     "social_core.pipeline.social_auth.associate_user",
#     "social_core.pipeline.social_auth.load_extra_data",
#     "social_core.pipeline.user.user_details",
# )

DOMAIN_NAME = "localhost"

# Email
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = "tmp/email-messages/"

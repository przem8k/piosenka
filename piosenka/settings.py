import os

from django.urls import reverse_lazy

PROJECT_PATH = os.path.join(os.path.abspath(os.path.split(__file__)[0]), "..")

if os.getenv("GAE_APPLICATION", None) or os.getenv("RELEASE", None):
    DEBUG = False

    # App Engine's security features ensure that it is safe to
    # have ALLOWED_HOSTS = ['*'] when the app is deployed.
    ALLOWED_HOSTS = ["*"]

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.getenv("PIOSENKA_DB_NAME"),
            "USER": os.getenv("PIOSENKA_DB_USER"),
            "PASSWORD": os.getenv("PIOSENKA_DB_PASSWORD"),
            "HOST": os.getenv("PIOSENKA_DB_HOST"),
        }
    }

    SECRET_KEY = os.getenv("PIOSENKA_SECRET_KEY")

    import google.cloud.logging

    client = google.cloud.logging.Client()
    client.get_default_handler()
    client.setup_logging()

    EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"
    ANYMAIL = {
        "MAILJET_API_KEY": os.getenv("PIOSENKA_MAILJET_API_KEY"),
        "MAILJET_SECRET_KEY": os.getenv("PIOSENKA_MAILJET_API_SECRET"),
    }
else:
    DEBUG = True
    if os.getenv("PROXY_TO_PROD"):
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "HOST": "127.0.0.1",
                "PORT": "5432",
                "NAME": os.getenv("PIOSENKA_DB_NAME"),
                "USER": os.getenv("PIOSENKA_DB_USER"),
                "PASSWORD": os.getenv("PIOSENKA_DB_PASSWORD"),
            }
        }
    else:
        # local sqllite file
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "piosenka.db",
            }
        }
    SECRET_KEY = "piosenka-local-dev-not-really-secret"

    MEDIA_ROOT = os.path.join(PROJECT_PATH, "site_media")

    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = "/tmp/django-emails"

DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_BUCKET_NAME = 'piosenka-media'
GS_LOCATION = 'media'
GS_DEFAULT_ACL = "publicRead"
MEDIA_URL = 'https://storage.googleapis.com/piosenka-media/media/'
THUMBNAIL_DEFAULT_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"

USE_TZ = True
TIME_ZONE = "Europe/Warsaw"
LANGUAGE_CODE = "pl"

SITE_ID = 1
USE_I18N = True
USE_L10N = True

# Where static files are served from by the dev server.
STATIC_ROOT = os.path.join(PROJECT_PATH, "static")

# URL prefix used for static files, in development and in production.
STATIC_URL = "/static/"

STATICFILES_DIRS = (
    ("", os.path.join(PROJECT_PATH, "assets")),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

COMPRESS_OFFLINE = True

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "piosenka.middleware.StaticPageFallbackMiddleware",
]

# For the middleware that serves the static pages for development.
# (in prod this is handled by mapping in app.yaml)
PZT_STATICPAGE_DIR = os.path.join(PROJECT_PATH, "out")

ROOT_URLCONF = "urls"

FILE_CHARSET = "utf-8-sig"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_PATH, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "piosenka.context_processors.to_review",
            ],
        },
    },
]

INSTALLED_APPS = (
    # Django.
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.admin",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.redirects",
    # Third-party.
    "easy_thumbnails",
    "compressor",
    # PzT.
    "base",
    "blog",
    "songs",
    "events",
    "piosenka",
    "content",
)

THUMBNAIL_ALIASES = {
    "songs.Song": {
        "scorethumb": {"size": (180, 0), "upscale": True},
    },
    "articles.Article.cover_image": {
        "cover": {"size": (600, 300), "crop": True, "upscale": True},
        "coverthumb": {"size": (420, 210), "crop": True, "upscale": True},
    },
    "songs.Artist.image": {
        "imagethumb": {"size": (0, 300), "upscale": True},
    },
    "songs.ArtistNote.image": {
        "imagethumb": {"size": (0, 300), "upscale": True},
    },
    "songs.SongNote.image": {
        "imagethumb": {"size": (0, 300), "upscale": True},
    },
}

INTERNAL_IPS = ("127.0.0.1",)

LOGIN_URL = reverse_lazy("hello")
LOGIN_REDIRECT_URL = reverse_lazy("index")
LOGOUT_REDIRECT_URL = reverse_lazy("index")

TEST_RUNNER = "django.test.runner.DiscoverRunner"

SITE = "https://www.piosenkaztekstem.pl"

DEFAULT_FROM_EMAIL = "noreply@piosenkaztekstem.pl"

# https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

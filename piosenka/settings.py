import os

from django.urls import reverse_lazy

if os.getenv('GAE_APPLICATION', None):
    DEBUG = False

    # App Engine's security features ensure that it is safe to
    # have ALLOWED_HOSTS = ['*'] when the app is deployed. 
    ALLOWED_HOSTS = ['*']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('PIOSENKA_DB_NAME'),
            'USER': os.getenv('PIOSENKA_DB_USER'),
            'PASSWORD': os.getenv('PIOSENKA_DB_PASSWORD'),
            'HOST': os.getenv('PIOSENKA_DB_HOST'),
        }
    }

    SECRET_KEY = os.getenv('PIOSENKA_SECRET_KEY')
    GOOGLE_API_BROWSER_KEY = os.getenv('PIOSENKA_GOOGLE_API_BROWSER_KEY')
    GOOGLE_API_SERVER_KEY = os.getenv('PIOSENKA_GOOGLE_API_SERVER_KEY')

    import google.cloud.logging
    client = google.cloud.logging.Client()
    client.get_default_handler()
    client.setup_logging()
else:
    DEBUG = True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'piosenka.db',
        }
    }
    SECRET_KEY = 'piosenka-local-dev-not-really-secret'
    GOOGLE_API_BROWSER_KEY = ''
    GOOGLE_API_SERVER_KEY = ''

USE_TZ = True
TIME_ZONE = 'Europe/Warsaw'
LANGUAGE_CODE = 'pl'

SITE_ID = 1
USE_I18N = True
USE_L10N = True

PROJECT_PATH = os.path.join(os.path.abspath(os.path.split(__file__)[0]), '..')

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'site_media', 'upload')

MEDIA_URL = '/site_media/upload/'

STATIC_ROOT = os.path.join(PROJECT_PATH, 'site_media', 'native')

STATIC_URL = '/site_media/native/'

SERVE_DIRECTLY_ROOT = os.path.join(PROJECT_PATH, 'site_media')

STATICFILES_DIRS = (('', os.path.join(PROJECT_PATH, 'static')),)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_OFFLINE = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

ROOT_URLCONF = 'urls'

FILE_CHARSET = 'utf-8-sig'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_PATH, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'piosenka.context_processors.to_review',
            ],
        },
    },
]

INSTALLED_APPS = (
    # Django.
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.redirects',
    # Third-party.
    'easy_thumbnails',
    'compressor',
    # PzT.
    'base',
    'blog',
    'articles',
    'songs',
    'events',
    'piosenka',
    'content',)

THUMBNAIL_ALIASES = {
    'songs.Song': {
        'scorethumb': {
            'size': (180, 0),
            'upscale': True
        },
    },
    'articles.Article.cover_image': {
        'cover': {
            'size': (600, 300),
            'crop': True,
            'upscale': True
        },
        'coverthumb': {
            'size': (420, 210),
            'crop': True,
            'upscale': True
        },
    },
    'songs.Artist.image': {
        'imagethumb': {
            'size': (0, 300),
            'upscale': True
        },
    },
    'songs.ArtistNote.image': {
        'imagethumb': {
            'size': (0, 300),
            'upscale': True
        },
    },
    'songs.SongNote.image': {
        'imagethumb': {
            'size': (0, 300),
            'upscale': True
        },
    },
}

INTERNAL_IPS = ('127.0.0.1',)

LOGIN_URL = reverse_lazy('hello')

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

SITE = 'https://www.piosenkaztekstem.pl'
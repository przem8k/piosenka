import os
from django.core.urlresolvers import reverse_lazy

try:
    from piosenka.settings_local import DEBUG
except ImportError:
    DEBUG = True

try:
    from piosenka.settings_local import DATABASES
except ImportError:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'piosenka.db',
        }
    }

try:
    from piosenka.settings_local import SECRET_KEY
except ImportError:
    SECRET_KEY = 'piosenka'

try:
    from piosenka.settings_local import ALLOWED_HOSTS
except ImportError:
    pass

try:
    from piosenka.settings_local import ADMINS
except ImportError:
    pass

try:
    from piosenka.settings_local import EMAIL_HOST
    from piosenka.settings_local import EMAIL_HOST_USER
    from piosenka.settings_local import EMAIL_HOST_PASSWORD
    from piosenka.settings_local import DEFAULT_FROM_EMAIL
    from piosenka.settings_local import SERVER_EMAIL
    from piosenka.settings_local import EMAIL_USE_TLS
except ImportError:
    pass

try:
    from piosenka.settings_local import S3BUCKET
except ImportError:
    pass

try:
    from piosenka.settings_local import AWS_PATH
except ImportError:
    AWS_PATH = 'aws'

try:
    from piosenka.settings_local import GOOGLE_MAPS_API_KEY
except ImportError:
    GOOGLE_MAPS_API_KEY = ''

try:
    from piosenka.settings_local import FB_APP_ID
    from piosenka.settings_local import FB_APP_SECRET
except ImportError:
    print('FB credentials not set')

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

STATICFILES_DIRS = (('', os.path.join(PROJECT_PATH, 'static')),
                    ('scripts', os.path.join(PROJECT_PATH, 'songs', 'scripts')),
                    os.path.join(PROJECT_PATH, 'client', 'assets'),)

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(PROJECT_PATH, 'client',
                                   'webpack-stats.json'),
        'IGNORE': ['.+\.hot-update.js', '.+\.map']
    },
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',)

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
    'webpack_loader',
    'facebook',
    # PzT.
    'base',
    'blog',
    'articles',
    'songs',
    'events',
    'frontpage',
    'piosenka',
    'content',)

THUMBNAIL_ALIASES = {
    'frontpage.CarouselItem.image': {
        'carousel': {'size': (900, 400),
                     'crop': True,
                     'upscale': True},
    },
    'songs.Song': {
        'scorethumb': {'size': (180, 0),
                       'upscale': True},
    },
    'articles.Article.cover_image': {
        'cover': {'size': (600, 300),
                  'crop': True,
                  'upscale': True},
        'coverthumb': {'size': (420, 210),
                       'crop': True,
                       'upscale': True},
    },
    'songs.Annotation.image': {
        'imagethumb': {'size': (0, 300),
                       'upscale': True},
    },
    'songs.Artist.image': {
        'imagethumb': {'size': (0, 300),
                       'upscale': True},
    },
    'songs.ArtistNote.image': {
        'imagethumb': {'size': (0, 300),
                       'upscale': True},
    },
}

INTERNAL_IPS = ('127.0.0.1',)

LOGIN_URL = reverse_lazy('hello')

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

SITE = 'http://www.piosenkaztekstem.pl'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'basic': {
            'format': '%(levelname)s %(asctime)s %(message)s',
        }
    },
    'handlers': {
        'actions_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'basic',
            'filename': os.path.join(PROJECT_PATH, 'actions.log')
        },
    },
    'loggers': {
        'actions': {
            'level': 'DEBUG',
            'handlers': ['actions_file'],
        },
    },
}

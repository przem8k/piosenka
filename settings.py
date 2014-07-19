import os

ADMINS = (
    ('Przemyslaw Pietrzkiewicz', 'pietrzkiewicz@gmail.com'),
)

MANAGERS = ADMINS

try:
    from settings_production import DATABASES
    from settings_production import SECRET_KEY
    from settings_production import ALLOWED_HOSTS

    from settings_production import EMAIL_HOST
    from settings_production import EMAIL_HOST_USER
    from settings_production import EMAIL_HOST_PASSWORD
    from settings_production import DEFAULT_FROM_EMAIL
    from settings_production import SERVER_EMAIL
    from settings_production import EMAIL_USE_TLS

    from settings_production import S3BUCKET
    from settings_production import GOOGLE_MAPS_API_KEY
    DEBUG = False
except ImportError:
    from settings_local import DATABASES
    from settings_local import SECRET_KEY

    from settings_local import GOOGLE_MAPS_API_KEY
    DEBUG = True

TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'Europe/Warsaw'
LANGUAGE_CODE = 'pl'

SITE_ID = 1
USE_I18N = True
USE_L10N = True

PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])

MEDIA_ROOT = os.path.join(PROJECT_PATH, "site_media", "upload")

MEDIA_URL = "/site_media/upload/"

STATIC_ROOT = os.path.join(PROJECT_PATH, "site_media", "native")

STATIC_URL = '/site_media/native/'

ALL_STATIC_ROOT = os.path.join(PROJECT_PATH, "site_media")

STATICFILES_DIRS = (
    ("", os.path.join(PROJECT_PATH, "static")),
    ("scripts", os.path.join(PROJECT_PATH, "songs", "scripts")),
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

PIPELINE_CSS = {
    'piosenka': {
        'source_filenames': (
            'css/style.css',
            'css/search.css',
            'third_party/bootstrap/css/bootstrap.css',
        ),
        'output_filename': 'css/piosenka.css',
    },
}

PIPELINE_JS = {
    'piosenka': {
        'source_filenames': (
            'third_party/jquery/jquery-2.1.1.js',
            'third_party/typeahead/typeahead-0.10.4.js',
            'third_party/bootstrap/js/bootstrap.js',
            'js/search.js',
        ),
        'output_filename': 'js/piosenka.js',
    },
}

PIPELINE_YUGLIFY_BINARY = os.path.join(PROJECT_PATH, 'node_modules/yuglify/bin/yuglify')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

if DEBUG:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

ROOT_URLCONF = 'urls'

FILE_CHARSET = "utf-8-sig"

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'frontpage.context.site_context',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'easy_thumbnails',
    'blog',
    'artists',
    'articles',
    'songs',
    'events',
    'frontpage',
    'dxlibrary',
    'south',
    'pipeline',
)

THUMBNAIL_ALIASES = {
    'frontpage.CarouselItem.image': {
        'carousel': {'size': (900, 400), 'crop': True, 'upscale': True},
    },
    'songs.Song': {
        'scorethumb': {'size': (180, 0), 'upscale': True},
    },
    'articles.Article.cover_image': {
        'cover': {'size': (600, 300), 'crop': True, 'upscale': True},
        'coverthumb': {'size': (420, 210), 'crop': True, 'upscale': True},
    }
}

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)

INTERNAL_IPS = ('127.0.0.1',)

import os

# Django settings both for production and developement environment

DEVELOPEMENT_SERVER_USERNAMES = ["dx",] # append your local username if You wish / need to

PRODUCTION_SETTINGS = not (os.getenv("USER") in DEVELOPEMENT_SERVER_USERNAMES)


DEBUG = not PRODUCTION_SETTINGS
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Przemyslaw Pietrzkiewicz', 'pietrzkiewicz@gmail.com'),
)

MANAGERS = ADMINS

if PRODUCTION_SETTINGS:
    DATABASES = {                   # update this section after production server migration
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'pg_5186',                      # Or path to database file if using sqlite3.
            'USER': 'pg_5186a',                      # Not used with sqlite3.
            'PASSWORD': 'swiatlemwoczy9',                  # Not used with sqlite3.
            'HOST': 'sql.dxhp.megiteam.pl',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '5435',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'playground',                      # Or path to database file if using sqlite3.
            'USER': 'playboy',                      # Not used with sqlite3.
            'PASSWORD': 'play',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Warsaw'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

import os
PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])

MEDIA_ROOT = os.path.join(PROJECT_PATH, "site_media", "upload")

MEDIA_URL = "/site_media/upload/"

STATIC_ROOT = os.path.join(PROJECT_PATH, "site_media", "native")

STATIC_URL = '/site_media/native/'

STATICFILES_DIRS = (
    ("", os.path.join(PROJECT_PATH, "static")),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'o@c*tih1vzy69-#wv16(^a7sgsv5l^vw7fah&+ttvyjyi@7)jr'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'website.urls'

FILE_CHARSET = "utf-8-sig"

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth', 
    'django.core.context_processors.debug',  
    'django.core.context_processors.media', 
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'songs.views.songs_context'
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, "templates"),
)

HAYSTACK_SITECONF = 'website.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_PATH, "index")

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',    
    'blog',
    'artists',
    'songs',
    'events',
    'dxlibrary',
    'haystack',
    'south',
)

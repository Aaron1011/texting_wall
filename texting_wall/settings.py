# Django settings for texting_wall project.

import os
from os import environ

DEBUG = True
TEMPLATE_DEBUG = DEBUG

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages",
"main.context_processors.analytics")

PUBLISH_KEY = "pub-8a8223f4-631c-4484-a118-2b01232307cc"
SUBSCRIBE_KEY = "sub-e754ed6b-133d-11e2-91f2-b58e6c804094"
SECRET = "sec-ZjcxZGVjNDAtZWQyMC00MGZmLTg1Y2MtNmJkNGE3YTJiYjlj"

TWITTER_CONSUMER_KEY = environ.get("TWITTER_CONSUMER_KEY", "")
TWITTER_CONSUMER_SECRET = environ.get("TWITTER_CONSUMER_SECRET", "")
TWITTER_ACCESS_TOKEN = environ.get("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_TOKEN_SECRET = environ.get("TWITTER_ACCESS_TOKEN_SECRET", "")

TWILIO_ACCOUNT_SID = environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = environ.get("TWILIO_AUTH_TOKEN", "")

OAUTH_CALLBACK = environ.get("OAUTH_CALLBACK","")

GOOGLE_ANALYTICS = False
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)


MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db.sqlite',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.abspath('staticfiles')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+303s__l2ataaceln$qfb7sp5qn%j5d&amp;_hrl_ijf^1+#dtduga'
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'texting_wall.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'texting_wall.wsgi.application'

TEMPLATE_DIRS = (
    os.path.abspath("templates"),
    os.path.abspath("main/templates")
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'south',


    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

env = environ.get("RACK_ENV", "dev")

if env == "production":
    DEBUG = False
    INSTALLED_APPS += ('gunicorn', "storages", "django_twilio",)
    import dj_database_url
    DATABASES['default'] =  dj_database_url.config()

    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    AWS_STORAGE_BUCKET_NAME = environ.get("AWS_STORAGE_BUCKET_NAME", "")
    AWS_ACCESS_KEY_ID = environ.get("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = environ.get("AWS_SECRET_ACCESS_KEY", "")
    TWILIO_ACCOUNT_SID = environ.get("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = environ.get("TWILIO_AUTH_TOKEN", "")
    STATIC_URL= 'http://s3.amazonaws.com/textingwall/'
    EMAIL_BACKEND = 'django_ses.SESBackend'
    INSTALLATION = "production"
    GOOGLE_ANALYTICS = True

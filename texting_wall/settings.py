
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
    "main.context_processors.analytics"
)

PUBNUB_PUBLISH_KEY = environ.get("PUBNUB_PUBLISH_KEY", "")
PUBNUB_SUBSCRIBE_KEY = environ.get("PUBNUB_SUBSCRIBE_KEY", "")
PUBNUB_SECRET = environ.get("PUBNUB_SECRET", "")

TWITTER_CONSUMER_KEY = "noiP40PTVLiZJYnBdXyoCw"
TWITTER_CONSUMER_SECRET = environ.get("TWITTER_CONSUMER_SECRET", "")
TWITTER_ACCESS_TOKEN = "879862038-f9vQhcogCEzbXad5d1YcRbcGeTMcnL8xl3SLRHIU"
TWITTER_ACCESS_TOKEN_SECRET = environ.get("TWITTER_ACCESS_TOKEN_SECRET", "")

TWILIO_ACCOUNT_SID = environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = environ.get("TWILIO_AUTH_TOKEN", "")

OAUTH_CALLBACK = environ.get("OAUTH_CALLBACK", "")

GOOGLE_ANALYTICS = False

WALL_EXPIRATION = 10

ADMINS = (
    ('Aaron Hill', 'aa1ronham@gmail.com'),
)


USER_THUMB_DIM = 48

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.abspath('media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.abspath('staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '+303s__l2ataaceln$qfb7sp5qn%j5d&amp;_hrl_ijf^1+#dtduga'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'middleware.ConsoleExceptionMiddleware'
)

ROOT_URLCONF = 'texting_wall.urls'

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
    'django.contrib.sitemaps',
    'main',
    'south',
    'django.contrib.admin',
    'django_twilio'

)

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
    INSTALLED_APPS += ('gunicorn', "storages")
    import dj_database_url
    DATABASES['default'] = dj_database_url.config()

    AWS_STORAGE_BUCKET_NAME = "textingwall"

    INSTALLATION = "production"
    GOOGLE_ANALYTICS = True

elif env == "test":
    INSTALLED_APPS += ('storages',)
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }


if env != "dev":
    STATICFILES_STORAGE = 'main.s3utils.StaticS3BotoStorage'
    DEFAULT_FILE_STORAGE = "main.s3utils.MediaS3BotoStorage"

    TWILIO_ACCOUNT_SID = "ACafdbf02572edd7c9dbdaf382a223274c"
    TWILIO_AUTH_TOKEN = environ.get("TWILIO_AUTH_TOKEN", "")

    AWS_ACCESS_KEY_ID = "AKIAJDPMOLSYHWGM4NYQ"
    AWS_SECRET_ACCESS_KEY = environ.get("AWS_SECRET_ACCESS_KEY", "")

    S3_URL = 'http://s3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
    STATIC_DIRECTORY = '/static'
    MEDIA_DIRECTORY = '/media'
    STATIC_URL = S3_URL + STATIC_DIRECTORY
    MEDIA_URL = S3_URL + MEDIA_DIRECTORY


try:
    from local_settings import *
except Exception, e:
    print e

import os
import sys

SITE_ROOT = os.environ.get('SITE_ROOT')

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'app_adimsayar',                    # Or path to database file if using sqlite3.
        'USER': 'app_adimsayar',                      # Not used with sqlite3.
        'PASSWORD': 'OypQd2X74VpWyAxK',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SHOW_ADS_HOMEPAGE = False
SHOW_ADS_MEAS = False



#    ,
#        'psql': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'adimsayar',                    # Or path to database file if using sqlite3.
#        'USER': 'postgres',                      # Not used with sqlite3.
#        'PASSWORD': 'sasko123',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Istanbul'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'tr-TR'

DEFAULT_CHARSET = 'utf-8'
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True


#import settings here
OVERLOAD_SITE = os.environ.get('OVERLOAD_SITE')
OVERLOAD_SITE_MODULE ="site_overloads" + "." + OVERLOAD_SITE
exec "from %s.settings import *" % (OVERLOAD_SITE_MODULE)


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)



MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'disable.DisableCSRF', 
    'django.middleware.locale.LocaleMiddleware',
    'languageMiddleware.setLanguageByOverloadSite',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'raven.contrib.django',
    'userprofile',
    'mining_platform',
    'social_auth',
    'core',
    'content',
    'contact',
    'meas',
    'device2',
    'statistics',
    'body_info',
    'diet',
    'login',
    'poll',
    'mailing',
    'badges',
    'venue',
    'score',
    'mobindex',
#    'mobsync',
    'tinyurl',
    'ad',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',   
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends', 
    'context_processors.site_overload', 
    'django.core.context_processors.request'
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

try:
    import django_coverage
    INSTALLED_APPS += ('django_coverage',)
except ImportError:
    pass

# START of django-profile specific options
I18N_URLS = False
DEFAULT_AVATAR = os.path.join(MEDIA_ROOT, 'generic.jpg')
AVATAR_WEBSEARCH = True
# 127.0.0.1:8000 Google Maps API Key
GOOGLE_MAPS_API_KEY = "ABQIAAAAhPOE3wMn6-73DioOcRWkQxRtKcszlIyU3IRTJzgOT3WJZ8EJ3BTdPjdAj07cQJJLrySiSh1DdB5qiw"

SENTRY_KEY = 'Rw2s/z6T0qoWPBXdZOy6grWaVPVzpE7nEJJ+TIXWDEaeWA8qLnb7uA=='

RAVEN_CONFIG = {
    'dsn': 'http://4d88504285f3452ca3e62109a3c44f3e:98ad98773d124bc4afcff100a5be2266@www.adimsayar.biz:9000/1',
    'register_signals': True,
}

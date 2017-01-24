import os

SITE_ROOT = os.environ.get('SITE_ROOT')

DOMAIN_NAME = 'www.alldaypedometer.com'

LANGUAGE_CODE = 'en'

GOOGLE_ANALYTICS_ID = 'UA-30059372-1'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT,'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

TEMPLATE_DIRS = (os.path.join(SITE_ROOT, "template"))

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'h8!ub4+%+msi58^%wv^+jj12($s9geiheienv&fitxh1(d+v0i'

PROJECT_DIR_NAME = os.environ.get('PROJECT_DIR_NAME')

ROOT_URLCONF = PROJECT_DIR_NAME+'.urls'

FACEBOOK_APP_ID = '263066070430718'
FACEBOOK_APP_SECRET = 'ea9bc9577fdbf715cf129826943f93ed'
FACEBOOK_APP_NAME = 'alldaypedometer'

AUTH_PROFILE_MODULE = 'core.profile'

# django-registration
ACCOUNT_ACTIVATION_DAYS = 7
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'alldaypedometer@gmail.com'
EMAIL_HOST_PASSWORD = 'cd89a9123'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'AllDayPedometer <alldaypedometer@gmail.com>'
LOGIN_REDIRECT_URL = '/'


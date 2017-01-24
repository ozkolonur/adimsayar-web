import os

SITE_ROOT = os.environ.get('SITE_ROOT')

DOMAIN_NAME = 'www.adimsayar.biz'

LANGUAGE_CODE = 'tr'

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

FACEBOOK_APP_ID = '147397685368778'
FACEBOOK_APP_SECRET = '27e191c129514d1d16ec32fa2ba5ca17'
FACEBOOK_APP_NAME = 'adimsayar_biz'

AUTH_PROFILE_MODULE = 'core.profile'

# django-registration
ACCOUNT_ACTIVATION_DAYS = 7
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'adimsayarbilgi@gmail.com'
EMAIL_HOST_PASSWORD = 'cd89a9123'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'Adimsayar <adimsayarbilgi@gmail.com>'


#YAHOO?
TWITTER_CONSUMER_KEY              = 'znqephhiqYHPFuIGhAth0w'
TWITTER_CONSUMER_SECRET           = 'Z5hE71pwwRCIYIYZM8cnsRbGbbm8PYAWIwxIdVyMEc'
FACEBOOK_APP_ID                   = '147397685368778'
FACEBOOK_API_SECRET               = '27e191c129514d1d16ec32fa2ba5ca17'
GOOGLE_OAUTH2_CLIENT_ID           = '827156880209.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET       = '_iVOCEP_3rkVQ_T7QVF8DnKi'
SOCIAL_AUTH_CREATE_USERS          = True
SOCIAL_AUTH_FORCE_RANDOM_USERNAME = False
SOCIAL_AUTH_DEFAULT_USERNAME      = 'uye_'
SOCIAL_AUTH_COMPLETE_URL_NAME     = 'socialauth_complete'
#SOCIAL_AUTH_USER_MODEL            = 'User'
SOCIAL_AUTH_ERROR_KEY             = 'socialauth_error'
FOURSQUARE_CONSUMER_KEY           = ''
FOURSQUARE_CONSUMER_SECRET        = ''
SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.misc.save_status_to_session',
    'login.pipeline.redirect_to_form',
    'login.pipeline.username',
    'social_auth.backends.pipeline.user.create_user',
    'login.pipeline.create_profile',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details'
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL          = '/login/form/'
LOGIN_REDIRECT_URL = '/login/done/'
LOGIN_ERROR_URL    = '/login/error/'

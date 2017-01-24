from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^http_get_sec/$', 'mining_platform.views.http_get_sec'),
    (r'^http_get/$', 'mining_platform.views.http_get'),
    (r'^test_new_user_fb/$', 'mining_platform.views.test_new_user_fb'),
    (r'^test_new_user_email/$', 'mining_platform.views.test_new_user_email'),
    (r'^authorize_user/$', 'mining_platform.views.authorize_user'),
    (r'^register_email_user/$', 'mining_platform.views.register_email_user'),
    (r'^reset_password_email/$', 'mining_platform.views.reset_password_email'),
    (r'^get_atom/$', 'mining_platform.views.get_atom'),
)    


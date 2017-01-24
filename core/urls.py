from django.conf.urls.defaults import patterns,  url
from django.views.generic.simple import direct_to_template,redirect_to



urlpatterns = patterns('core.views',
    url(r'^send_mail/$', 'dont_mail' , name="dont_mail"),
    url(r'^test_lang/$', 'test_lang' , name="test_lang"),
    url(r'^user_delete/$',  'user_delete' , name="user_delete"),
    url(r'^authorize_user/$', 'authorize_user', name="authorize_user"),
    url(r'^register_email_user/$', 'register_email_user', name="register_email_user"),
    url(r'^reset_password_email/$', 'reset_password_email', name="reset_password_email"),
    url(r'^my_badges/$',  'my_badges' , name="my_badges"),
)

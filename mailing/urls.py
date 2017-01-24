from django.conf.urls.defaults import patterns,  url
from django.views.generic.simple import direct_to_template,redirect_to

urlpatterns = patterns('mailing.views',
    url(r'^$',    'mailing_index', name="mailing_index"),
    url(r'^preview/(?P<mailing_id>\d+)/$', 'preview', name='mailing_preview'),
    url(r'^tracking_img/(?P<user_id>\d+)/(?P<mailing_id>\d+)/$', 
        'tracking_img', name='tracking_img'),
    url(r'^bounces/$', 'bounces', name='bounces'),
    url(r'^complaints/$', 'complaints', name='complaints'),
)

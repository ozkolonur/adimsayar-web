from django.conf.urls.defaults import patterns,  url
from django.views.generic.simple import direct_to_template,redirect_to

urlpatterns = patterns('mobsync.views',
    url(r'^config/$', 'config_sync', name="config_sync"),
    url(r'^latest_version/$', 'latest_version', name="latest_version"),
)

from django.conf.urls.defaults import patterns,  url
from django.views.generic.simple import direct_to_template,redirect_to

urlpatterns = patterns('venue.views',
    url(r'^list/$',    'list', name="list"),
    url(r'^checkin/$',    'checkin', name="checkin"),
)

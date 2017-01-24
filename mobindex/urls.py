from django.conf.urls.defaults import patterns,  url
from django.views.generic.simple import direct_to_template,redirect_to

urlpatterns = patterns('mobindex.views',
    url(r'', 'mobile_url_parser', name="mobile_url_parser"),
)

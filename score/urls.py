from django.conf.urls.defaults import patterns,  url
from django.views.generic.simple import direct_to_template,redirect_to

urlpatterns = patterns('score.views',
    url(r'^near_20/$', 'get_near_20', name="get_near_20"),
)

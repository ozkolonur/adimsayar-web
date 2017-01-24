from django.conf.urls.defaults import patterns, url, include
from login.views import home, done, logout, error, form, set_nickname

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^form/$', form, name='form'),
    url(r'^set_nickname/$', set_nickname, name='set_nickname'),
    url(r'', include('social_auth.urls')),
)

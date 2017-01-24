from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template,redirect_to

urlpatterns = patterns('content.views',
     url(r'^$', 'index', name='index'),
     url(r'^howitworks/$', 'get_content_page', {'name':'hows'}, name='howitworks'),
     url(r'^devices/$', 'device',name='devices'),
     url(r'^support/$', 'support', name='support'),
     url(r'^pic_install/$', 'pic_install', name='pic_install'),
     url(r'^faq_walking/$', 'faq_walking', name='faq_walking'),
     url(r'^glysemic_index/$', 'glysemic_index', name='glysemic_index'),
     url(r'^mobile_install/$', 'mobile_install', name='mobile_install'),
     url(r'^privacy/$', 'privacy', name='privacy'),
     url(r'^get/$', 'get', name='get'),
     url(r'^get_content_page/$', 'get_content_page', name='get_content_page'),
     url(r'^get_content_frame/$', 'get_content_frame', name='get_content_frame'),
     #url(r'^mobindex/$', 'mobindex',name='mobindex'),
)
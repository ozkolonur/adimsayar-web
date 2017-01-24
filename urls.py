from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin 
from django.views.generic.simple import direct_to_template,redirect_to
from django.conf import settings
from userprofile.views import get_profiles
import os.path
KlasorYolu = os.path.dirname(__file__)
admin.autodiscover()

#urlpatterns = patterns('',
#     url(r'^automatic_emails/$', 'automatic_emails.views.index', name='automatic_emails'),
#)

#TODO move these to urls.py in content dir
urlpatterns = patterns('content.views',
     url(r'^$', 'index', name='index'),
     url(r'^howitworks/$', 'get_content_page', {'name':'howitworks', 'locale':'tr'}, name='howitworks'),
     url(r'^devices/$', 'get_content_page', {'name':'devices', 'locale':'tr'}, name='devices'),
     url(r'^support/$',  'get_content_page', {'name':'support', 'locale':'tr'}, name='support'),
     url(r'^pic_install/$', 'get_content_page', {'name':'pic_install', 'locale':'tr'}, name='pic_install'),
     url(r'^faq_walking/$', 'get_content_page', {'name':'faq_walking', 'locale':'tr'}, name='faq_walking'),
     url(r'^glysemic_index/$', 'get_content_page', {'name':'glysemic_index', 'locale':'tr'}, name='glysemic_index'),
     url(r'^mobile_install/$', 'get_content_page', {'name':'mobile_install', 'locale':'tr'}, name='mobile_install'),
     url(r'^privacy/$', 'get_content_page', {'name':'privacy', 'locale':'tr'}, name='privacy'),
     url(r'^yukle/$',  direct_to_template,{'template':'install.html'}),
     url(r'^sds/$', 'sds', name='sds'),
     url(r'^action.aspx/$', 'save_action', name='save_action'),
     url(r'^get/$', 'get', name='get'),
     url(r'^get_content_page/$', 'get_content_page', {'name':None, 'locale':'tr'},name='get_content_page'),
     url(r'^get_content_frame/$', 'get_content_frame', {'name':None, 'locale':'tr'},name='get_content_frame'),
     #url(r'^badges/', include('badges.urls')),
     #url(r'^mobindex/$', 'mobindex',name='mobindex'),
)

urlpatterns += patterns('',
     url(r'^meas/', include('meas.urls'), ),
     url(r'^profile/', include('core.urls'), ),
     url(r'^statistics/', include('statistics.urls'), ),
     url(r'^body_info/', include('body_info.urls'), ),
     url(r'^venues/', include('venue.urls'), ),
     url(r'^mailing/', include('mailing.urls'), ),
     url(r'^diet/', include('diet.urls'),),
     url(r'^login/', include('login.urls'),),
     url(r'^poll/', include('poll.urls'),),
     url(r'^url/', include('tinyurl.urls'),),
     url(r'^ad/', include('ad.urls'),),
     (r'^mining_platform/', include("mining_platform.urls")),
     (r'^http_xml_test/$',  direct_to_template,
            { 'template': 'http_xml_test.html' }, 'http_xml_test'),
     url(r'^mobindex/', include('mobindex.urls'),),
     url(r'^mobsync/', include('mobsync.urls'),),
     url(r'^score/', include('score.urls'),),
    # Profile application
     (r'^accounts/', include('userprofile.urls')),
     url(r'^contact/', include('contact.urls'),  ),
     # Admin (not really needed)
     (r'^admin/doc/', include('django.contrib.admindocs.urls')),
     (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(KlasorYolu, 'media/')}),
   
   )

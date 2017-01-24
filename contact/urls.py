from django.conf.urls.defaults import *
urlpatterns = patterns('',    
    url(r'thankyou/', 'contact.views.thankyou'),
    url(r'^$', 'contact.views.contactview',name='contact'),
)

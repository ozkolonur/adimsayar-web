# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template,redirect_to

urlpatterns = patterns('ad.views',
     url(r'^request/$', 'request', name='adrequest'),
)
# -*- coding: utf-8 -*-

# Create your views here.
from django.shortcuts import render_to_response,HttpResponse


def request(request):
    return HttpResponse('<html><body style="margin:0px;"><img src="http://www.adimsayar.com/site_media/images/banner_mobile_320.jpg" /></body></html>')

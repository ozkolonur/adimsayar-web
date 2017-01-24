# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

# Create your views here.
def mobile_url_parser(request):
    target = request.POST.get('target',None)
    if target == "ios":
        subdomain = "."
    elif target == "android":
        subdomain = "file:///android_asset"
    else:
        subdomain = ""
    return render_to_response(request.path[1:],{'subdomain':subdomain}, 
            context_instance=RequestContext(request))


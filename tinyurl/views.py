from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import Http404

from tinyurl.models import TinyURL

def redirect(request, hash):
    try:
        tinyurl = get_object_or_404(TinyURL, hash=hash)
        tinyurl.clicks += 1
        tinyurl.save()
        return HttpResponseRedirect(tinyurl.url)
    except Http404:
        pass
    
    return HttpResponseRedirect("http://www.adimsayar.com")

from django.utils import translation
from django.conf import settings

class setLanguageByOverloadSite(object):
    def process_request(self, request):
		if settings.OVERLOAD_SITE == 'adimsayar':
			request.LANGUAGE_CODE = 'tr'
			translation.activate('tr')
		elif settings.OVERLOAD_SITE == 'alldaypedometer':
			request.LANGUAGE_CODE = 'en'
			translation.activate('en')
		else:
			request.LANGUAGE_CODE = 'tr'
			translation.activate('tr')
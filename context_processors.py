from django.conf import settings # import the settings file

def site_overload(context):
	# return the value you want as a dictionnary. you may add multiple values in there.
	return {'OVERLOAD_SITE': settings.OVERLOAD_SITE, 
			  'DOMAIN_NAME': settings.DOMAIN_NAME, 
			  'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
			  'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID,
			   }


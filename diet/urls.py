from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('diet.views',
    url(r'^$', 'diet_list', name="diet_list"),
    url(r'^diet_select/(?P<diet_id>\d+)/$', 'diet_select', name='diet_select'),
	url(r'^rating/$',  'rating' , name="rating"),
    url(r'^sync/$', 'diet_sync', name="diet_sync"),

    )

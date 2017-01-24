from django.conf.urls.defaults import patterns,  url
from django.views.generic.simple import direct_to_template,redirect_to



urlpatterns = patterns('statistics.views',
    url(r'^$',   'index', name="statistics"),
    url(r'^my_bmi/$',  'bmi_index' , name="bmi_statistics"),
    url(r'^bmi_tool/$',  'bmi_tool' , name="bmi_tool"),
    url(r'^age_vs_user/$'	, 'age_vs_user' , name="age_vs_user"),
    url(r'^bmi_vs_user/$'	, 'bmi_vs_user' , name="bmi_vs_user"),
    url(r'^age_vs_provinces/$'	, 'age_vs_provinces' , name="age_vs_provinces"),
    url(r'^daily_stats/$'	, 'daily_stats' , name="daily_stats"),
)

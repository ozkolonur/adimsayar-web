from django.conf.urls.defaults import patterns,  url
from django.views.generic.simple import direct_to_template,redirect_to

urlpatterns = patterns('body_info.views',
    url(r'^bmi_meter/$',    'bmi_meter', name="statistics"),
    url(r'^bmi_meter_widget/$',  'bmi_meter_widget', name="bmi-meter-widget"),
    url(r'^daily_calories/$',  'daily_calories', name="daily_calories"),
    url(r'^update/$', 'update', name="update"),
    url(r'^del_body_info/(?P<body_info_id>\d+)', 'del_body_info',name="del_body_info"),
)

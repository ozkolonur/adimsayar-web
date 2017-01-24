from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template,redirect_to
from django.conf import settings



urlpatterns = patterns('meas.views',
    url(r'^$',    'meas_index',  name="meas"),
    url(r'^fbtest/$',    direct_to_template, {'template': 'meas/fbtest.html'}, name="fbtest"),
    url(r'^steps/$', 'steps_today', name="steps"),
    url(r'^points/$', 'points', name="points"),
    url(r'^total/$', 'steps_monthly', name="total"),
    url(r'^calories/$', 'calories', name="calories"),
    url(r'^bmi/$', 'weight' ,name="bmi"),
    url(r'^bmi_image/$', 'bmi_image' ,name="bmi_image"),
    url(r'^try/$', 'try_function' ,name="try"),
    url(r'^grandtotal/$', 'grand_total_steps' ,name="grand_total"),
    url(r'^channel/$',  direct_to_template,{'template':'meas/channel.html'}),
    url(r'^feeds/$', 'check', name="post_feed"),
    url('^fbapp/$', redirect_to, {'url': 'http://apps.facebook.com/'+settings.FACEBOOK_APP_NAME+'/'},name="fbapp" ),
    url('^redirect/$', redirect_to, {'url': '/accounts/login?next=/meas/fbapp/'},name="redirect" ),
    url(r'^mobil/$', 'mobil_exp' ,name="mobil"),
    url(r'^support/$', 'meas_support' ,name="meas_support"),
    url(r'^tracker/$', 'tracker' ,name="meas_tracker"),
    url(r'^tracker2/$',  direct_to_template,{'template' : 'tracker/tracker.html'} , name="tracker"),
    url(r'^tracker_image/$',  'pil_image' , name="pil_image"),
    url(r'^tracker_image_share/$',  'pil_share' , name="pil_share"),
    url(r'^version/$', 'version', name='version'),
    url(r'^users_top/$', 'users_top', name='users_top')
)

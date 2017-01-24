from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('poll.views',
    url(r'^$', 'poll_widget', name="poll_link"),
    url(r'^answer/$', 'answer', name="answer_link"),
    url(r'^question/(?P<poll_id>\d+)/$', 'poll_question', name='poll_question'),
    url(r'^result/(?P<poll_id>\d+)/$', 'poll_result', name='poll_result'),
)
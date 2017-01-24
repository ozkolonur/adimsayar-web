from django.shortcuts import render_to_response,HttpResponse
from content.models import *
from meas.models import *
from statistics.models import Statistics
from django.contrib.auth.models import User
from userprofile.models import BaseProfile
from django.template import RequestContext
from django.conf import settings
from poll.models import Answer,Question
import tempfile
import shutil

diet_suggestion = DietSuggestion.objects.all()
calories_suggestion = CaloriesSuggestion.objects.order_by('?')[:2]


def index(request):
	try:
		question = Question.objects.order_by('?')[0]
		answers = Answer.objects.filter(question=question)
		answers.reverse()
		grand_total=Statistics.objects.get()
	except:
		grand_total=0
	if settings.OVERLOAD_SITE == 'adimsayar':
		news = News.objects.filter(locale='tr').order_by('-date_time')
	elif settings.OVERLOAD_SITE == 'alldaypedometer':
		news = News.objects.filter(locale='en').order_by('-date_time')
	else:
		news = News.objects.all().order_by('-date_time')
	content = Content.objects.filter(pk=1)
	if request.user.is_authenticated():
		user = User.objects.get(pk=request.user.pk)
	else:
		user = User.objects.filter()
	response = render_to_response('index.html', {'content':content,
                                                 'user':user,
                                                 'news':news,
                                                 'grand_total':grand_total,
                                                 'question':question,
                                                 'answers':answers,
                                                 'show_ads':settings.SHOW_ADS_HOMEPAGE,
                            }, context_instance=RequestContext(request))
	response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'
	return response


FILE_UPLOAD_DIR = '/tmp/'

def handle_uploaded_file(source):
    fd, filepath = tempfile.mkstemp(prefix=source.name, dir=FILE_UPLOAD_DIR)
    with open(filepath, 'wb') as dest:
        shutil.copyfileobj(source, dest)
    return filepath

def sds(request):
	import pdb; pdb.set_trace()
	handle_uploaded_file(request.FILES['AllInfo.txt'])
	return HttpResponse("helo")

def save_action(request):
    odemeid = request.GET.get('odemeid',None)
    tutar = request.GET.get('tutar',None)
    if odemeid and tutar:
        try:
            tmp = ActionMsg(tutar=tutar, odemeid=odemeid)
            tmp.save()
            return HttpResponse("OK,odemeid:"+odemeid+" tutar="+tutar)
        except Exception,err:
            return HttpResponse("FAIL")
    else:
        return HttpResponse("FAIL")

def get(request):
	name = request.GET.get('name', None)
	locale = request.GET.get('locale', None)
	content = None
	if name:
		content = Content.objects.filter(page=name)
		if (content.count() > 1) and (locale):
			content = Content.objects.filter(page=name, locale=locale)
		return render_to_response('get_content.html', {'content':content},context_instance=RequestContext(request))
	else:
		return HttpResponse("No content")

def get_content_page(request, name, locale):
	show_ads = False
	ads = request.GET.get("ads", "")
	if (ads == "yes"):
		show_ads = True
	if name == None:
		name = request.GET.get('name', None)
	if locale == None:
		locale = request.GET.get('locale', None)
	content = None
	if name:
		content = Content.objects.filter(page=name)
		if (content.count() > 1) and (locale):
			content = Content.objects.filter(page=name, locale=locale)
		return render_to_response('get_content_page.html', {'content':content, 'show_ads':show_ads},context_instance=RequestContext(request))
	else:
		return HttpResponse("No content name:"+ name + " locale:" + locale)

def get_content_frame(request, name, locale):
	name = request.GET.get('frame', None)
	return render_to_response('get_content_frame.html', {'frame':name},context_instance=RequestContext(request))


def mobindex(request):
	return HttpResponse("This is mobindex");

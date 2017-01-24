from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from core.models import Profile
from django.http import HttpResponse, HttpResponseRedirect

from social_auth import __version__ as version
from social_auth.utils import setting

from django.contrib.auth.models import User

def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return HttpResponseRedirect('done')
    else:
        return render_to_response('login/home.html', {'version': version},
                                  RequestContext(request))


@login_required
def done(request):
    """Login complete view, displays user data"""
    ctx = {
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    return HttpResponseRedirect('/')


def error(request):
    """Error view"""
    return HttpResponseRedirect('/')


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')

def set_nickname(request):
    target = request.GET.get('target','/meas/points')
    username = request.POST.get('username', None)
    if request.method == 'POST' and username:
        user_is_exist = True
        try:
            tmp = User.objects.get(username=username)
        except User.DoesNotExist:
            user_is_exist = False
        #TODO localization
        if user_is_exist:
            return render_to_response('login/set_nickname.html',
                {'err_msg':'Bu rumuz daha once alinmis'}, RequestContext(request))
        else:
            user = User.objects.get(id=request.user.id)
            user.username = username
            user.save()
            prof = Profile.objects.get(user=user)
            prof.nickname_is_set = True
            prof.save()
            return HttpResponseRedirect(target)
    elif request.method == "GET":
        user = User.objects.get(id=request.user.id)
        prof = Profile.objects.get(user=user)
        if prof.nickname_is_set:
            return HttpResponseRedirect(target)
        else:
            return render_to_response('login/set_nickname.html',
                {'err_msg':None}, RequestContext(request))
    else:
        return render_to_response('login/set_nickname.html', 
            {'err_msg':'Hata'}, RequestContext(request))

def form(request):
	if request.method == 'POST' and request.POST.get('username'):
		username = request.POST.get('username')
		user_is_exist = True
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			user_is_exist = False
		#TODO localization
		if user_is_exist:
			return render_to_response('login/form.html', {'err_msg':'Bu rumuz daha once alinmis'}, RequestContext(request))
		else:
			name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
			request.session['saved_username'] = request.POST['username']
			backend = request.session[name]['backend']
			return redirect('socialauth_complete', backend=backend)
	return render_to_response('login/form.html', {}, RequestContext(request))

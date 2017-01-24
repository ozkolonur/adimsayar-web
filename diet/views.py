from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from diet.models import Diet, DietDefinition, Atom
from core.models import Profile
from content.models import Content
from django.core import serializers
from diet.models import DietDefinition

def diet_list(request):
	if request.user.is_authenticated():
		profile = Profile.objects.filter(user=request.user)
		user_diet = profile[0].diet
		if user_diet:
			diet_inst = Diet.objects.get(user = request.user)
			return render_to_response('meas/diet_prog.html',{'diet':diet_inst},
									context_instance=RequestContext(request))
		else:
			sliders = Content.objects.filter(page__contains="slide")
			diets = DietDefinition.objects.all()
			return render_to_response('meas/diet_prog.html',{'diets':diets,'sliders':sliders[0]},
						context_instance=RequestContext(request))
	else:
		return HttpResponsePermanentRedirect('/accounts/login?next=/meas/steps/')
	
def diet_select(request,diet_id):
	diet_definition = DietDefinition.objects.get(pk=diet_id)
	diet = Diet(user=request.user, diet_definition = diet_definition)
	diet.save()
	# set weight....
	profile = Profile.objects.filter(user=request.user)
	profile.update(diet=diet)
	return HttpResponseRedirect('/diet/')

def rating(request):
	if request.method == 'POST':
		diet_id = request.POST.get('idBox')
		rate = request.POST.get('rate')
		diet = DietDefinition.objects.get(pk=diet_id)
		diet_rate = diet.diet_rate+int(rate)
		rate_count = diet.rate_count + 1
		diet.diet_rate = diet_rate
		diet.rate_count = rate_count
		diet.save()
		return HttpResponse('ok')
	else:
		return HttpResponseRedirect('/')
	

def diet_sync(request):
    definitions = DietDefinition.objects.all()
    data = serializers.serialize('json', definitions)
    return HttpResponse(data, mimetype='application/json')

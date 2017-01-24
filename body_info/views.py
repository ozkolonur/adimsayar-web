# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from core.models import Profile
from content.models import Content
from body_info.models import BodyInfo
from django.core.urlresolvers import reverse

#	base_url = "https://chart.googleapis.com/chart?cht=gom&chco=FF0000,FFFF00,00FF00,FFFF00,FFAA00,FF4400,FF0000&chxt=x,y&chxl=0:|Normal|1:|Zay%C4%B1f|Normal|Fazla%20Kilolu|%C5%9Ei%C5%9Fman|A%C5%9F%C4%B1r%C4%B1%20%C5%9Ei%C5%9Fman"
# Create your views here.
MIN_BMI_PRIME = float(0.60)
MAX_BMI_PRIME = float(1.60)
MIN_BMI = 15
MAX_BMI = 40

def get_bmi_text(bmi):
	if bmi < 16.00:
		res = "Zayıf"
	elif bmi >= 16.00 and bmi <= 25:
		res = "Normal"
	elif bmi > 25.00 and bmi <= 30:
		res = "Hafif Kilolu"
	elif bmi > 30.00:
		res = "Aşırı Kilolu"
	else:
		res = "Error:bmi_text"
	return res


def bmi_meter_widget(request):
	if ( result == "OK" ):
		return render_to_response('body_info/bmi-meter.html',{ 'bmi_img_url': bmi_img_url, 'cur_bmi': cur_bmi }, context_instance=RequestContext(request))
	else:
		return HttpResponse(result)

def update(request):
	if not request.POST:
		return HttpResponse("Hata")
	gender = request.POST.get('gender', None)
	age = request.POST.get('age', None)
	height = request.POST.get('height', None)
	weight = request.POST.get('weight', None)
	lifestyle = request.POST.get('lifestyle', None)
	body_info = BodyInfo(user=request.user)
	if gender == "M":
		body_info.gender = "M"
	elif gender == "F":
		body_info.gender = "F"
	if age:
		body_info.age = int(age)
	if height:
		body_info.height = int(height)
	if weight:
		body_info.weight = int(weight)
		body_info.weight_float = float(weight)
	if lifestyle:
		body_info.lifestyle = int(lifestyle)+1
	body_info.save()
	return HttpResponse("Kaydedildi")

def del_body_info(request,body_info_id):
    if request.user.is_authenticated():
        body_info = BodyInfo.objects.get(id=body_info_id)
        if body_info.user.id == request.user.id:
            body_info.delete()
        return HttpResponseRedirect(reverse('bmi'))
    else:
        return HttpResponseRedirect(reverse('index'))


def bmi_meter(request):
	bmi_prime = request.GET.get('bmi_prime', None)
	bmi = request.GET.get('bmi', None)
	divsw = request.GET.get('divsw', None)
	divsh = request.GET.get('divsh', None)
	result, bmi_img_url, cur_bmi = get_bmi_widget(bmi_prime, bmi, divsw, divsh)
	if ( result == "OK" ):
		return render_to_response('body_info/bmi-meter.html',{ 'bmi_img_url': bmi_img_url, 'cur_bmi': cur_bmi }, context_instance=RequestContext(request))
	else:
		return HttpResponse(result)

def get_bmi_widget(bmi_prime, bmi, divsw, divsh):
	base_url = "https://chart.googleapis.com/chart?cht=gom&chco=FF0000,FFFF00,00FF00,FFFF00,FFAA00,FF4400,FF0000&chxt=x,y&"
	result = "FAIL"
	#validate bmi_float
	if bmi_prime:
		try:
			bmi_prime_float = float(bmi_prime)
		except:
			bmi_prime_float = MIN_BMI_PRIME
		if bmi_prime_float >= MIN_BMI_PRIME and bmi_prime_float <= MAX_BMI_PRIME:
			bmi_float = bmi_prime_float * 25
	elif bmi:
		try:
			bmi_float = float(bmi)
		except:
			bmi_float = MIN_BMI
		if bmi_float < MIN_BMI and bmi_float > MAX_BMI:
			bmi_float = MIN_BMI
	else:
		return "ERROR:BMI", None, None


	#validate div sizes
	divsw_int = 400
	divsh_int = 220
	if divsw and divsh:
		try:
			divsw_int = int(divsw)
			divsh_int = int(divsh)
		except:
			return "ERROR:CHS", None, None
	else:
		divsw_int = 400
		divsh_int = 220

	# get text according to bmi
	cur_bmi_text = get_bmi_text(bmi=bmi_float)
	axis_value = ((bmi_float-15.00)/25)*100
	img_url = base_url + "&chd=t:%d&chs=%dx%d&chxr=1,15,40,5&chxl=0:|%s|" % (axis_value, divsw_int, divsh_int, cur_bmi_text)
	cur_bmi = "%.2f" % (bmi_float)

	result = "OK"
	return result, img_url, cur_bmi

def daily_calories(request):
    """
    mailden gelen kullanicilar icin bmi index sayfasi
    """
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login/?next=/body_info/daily_calories')
    error=""
    age=""
    weight=""
    height=""
    is_male=""
    is_female=""
    try:
        profile = Profile.objects.filter(user = request.user)
        profile = profile[0]
        if profile.age:
            age=profile.age
        else:
            age=""
        if profile.weight:
            weight=profile.weight
        else:
            weight=""
        if profile.height:
            height=profile.height
        else:
            height=""
        if profile.gender == "M":
            is_male="checked"
        if profile.gender == "F":
            is_female="checked"
    except:
        pass
    return render_to_response('body_info/daily_cal.html',
          			{'error':error ,'user':request.user, 'age':age, 'height':height, 'weight':weight, 'is_male':is_male, 'is_female':is_female },context_instance=RequestContext(request))



# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from meas.models import *
from statistics.models import Statistics, HttpReq
from core.models import Profile
from userprofile.models import BaseProfile
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime,timedelta
from django.db.models.signals import post_save
from django.core.cache import cache
from django.contrib.auth import authenticate
import time, cgi, urllib, urllib2
import simplejson as json
import random
import md5
import hashlib
import unicodedata
from core.models import Location, Country, City, Isp
from diet.models import Diet,Atom
from django.core import serializers
from device2.models import Device2, Product, Model, Manufacturer

class invalidRequest(Exception):
	pass

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip


def access_control(access_md5,device_id,request):
	return True
	if (device_id and access_md5 and request):
		url=request.build_absolute_uri()
		total = len(url) -39

		#WORKAROUND: some android app versions calculates wrong md5
		if (len(access_md5) == 31):
			access_md5 = "0"+access_md5
			total = total+1
		elif (len(access_md5) == 30):
			access_md5 = "00"+access_md5
			total = total+2

		secretstr='erdex'
		total = int(total) + 10000
		total = str(total)[1:]
		key=secretstr+ '|' +str(total)+ '|' +device_id
		access =hashlib.md5(key).hexdigest()
	if (access_md5 == access):
		return True	


def strip_accents(user):
	user_unicode = unicode(user)
	strip= ''.join((c for c in unicodedata.normalize('NFD', user_unicode) if unicodedata.category(c) != 'Mn'))
	return strip.lower()		

def authorize_user(request):
	try:
		email = request.GET.get('email', '')
		password = request.GET.get('key', '')
		user = User.objects.get(email=email)
		result = authenticate(username=user.username,password=password)
		if result is not None:
			return HttpResponse("OK")
		else:
			return HttpResponse("FAIL")
	except:
		return HttpResponse("FAIL")

def register_email_user(request):
		email = request.GET.get('email', '')
		key = request.GET.get('key', '')
		key_int = int(key)
		if ((key_int - 33900) != len(email)):
			return HttpResponse("FAIL")
		random_pass = str(random.randint(100000, 999999))
		user,created = User.objects.get_or_create(username=email, email=email)
		user.set_password(random_pass)
		user.save()
		profile, created = Profile.objects.get_or_create(user=user)
		profile= Profile.objects.filter(pk=profile.id)
		profile.update()
		html_content = render_to_string('meas/new_user_email.html', {'user':user,'random_pass':random_pass}) 
		text_content = strip_tags(html_content)
		subject, from_email, to = 'Adımsayar Üyelik Bilgileriniz.', 'adimsayarbilgi@gmail.com', email
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
		return HttpResponse("OK")

def reset_password_email(request):
	try:
		email = request.GET.get('email', '')
		random_pass = str(random.randint(100000, 999999))
		user = User.objects.get(email=email)
		user.set_password(random_pass)
		user.save()
		profile, created = Profile.objects.get_or_create(user=user)
		profile= Profile.objects.filter(pk=profile.id)
		profile.update()
		html_content = render_to_string('meas/new_user_email.html', {'user':user,'random_pass':random_pass}) 
		text_content = strip_tags(html_content)
		subject, from_email, to = 'Adımsayar Üyelik Bilgileriniz.', 'adimsayarbilgi@gmail.com', email
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
		return HttpResponse("islem tamam, yeni sifre email adresinize gonderildi")
	except:
		return HttpResponse("islem basarisiz")


def test_new_user_fb(request):
	    html_content = render_to_string('meas/new_user_fb.html') 
	    text_content = strip_tags(html_content)
	    subject, from_email, to = 'Adımsayar Üyelik Bilgileriniz.', 'adimsayarbilgi@gmail.com', 'ozkolonur@gmail.com'
	    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	    msg.attach_alternative(html_content, "text/html")
	    msg.send()
	    return HttpResponse("Mail sent")

def test_new_user_email(request):
	    html_content = render_to_string('meas/new_user_email.html') 
	    text_content = strip_tags(html_content)
	    subject, from_email, to = 'Adımsayar Üyelik Bilgileriniz.', 'adimsayarbilgi@gmail.com', 'ozkolonur@gmail.com'
	    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	    msg.attach_alternative(html_content, "text/html")
	    msg.send()
	    return HttpResponse("Mail sent")


def user_control_fb(request, access_key, email,height,weight,age,gender):
	try:			
	    user = User.objects.get(email=email)
	    fb_token = UserAssociation.objects.get(user=user)
	    profile = Profile.objects.get(user=user)
	    if (True): #was if (fb_token.token==access_key):
		    if (profile.height==height and profile.weight==weight and profile.age==age and profile.gender==gender):
			    return True
		    else:
			    profile = Profile.objects.filter(user=user)
			    try:
			        profile.update(height=height,weight=weight,age=age,gender=gender, ip_addr = get_client_ip(request))
			    except:
			        pass
			    return True	
	    else:
		    fb_token = UserAssociation.objects.filter(user=user)
		    fb_token.update(token=access_key)
		    return True	
	except:
		try:
			user = User.objects.get(email=email)
			profile = Profile.objects.get(user=user)
			if (profile.height==height and profile.weight==weight and profile.age==age and profile.gender==gender):
				return True
			else:
				profile = Profile.objects.filter(user=user)
				try:
					profile.update(height=height,weight=weight,age=age,gender=gender, ip_addr = get_client_ip(request))
				except:
					pass
				return True	
		except:
			access_token = access_key
			me_json = urllib.urlopen("https://graph.facebook.com/me?" +
											urllib.urlencode(dict(access_token=access_token)))
			fb_profile = json.load(me_json)
			username = fb_profile['first_name']+'-'+fb_profile['last_name']+'-'+fb_profile['id']
			username = strip_accents(username)
			user = User(username=username,
			email=fb_profile['email'],
			first_name=fb_profile['first_name'], 
			last_name=fb_profile['last_name'])
			user.set_unusable_password()
			user.save()
			profile, created = Profile.objects.get_or_create(user=user)
			profile.height = height
			profile.weight = weight
			profile.age = age
			profile.save()
#			We should find another way of updating access_token
#			fb_record=UserAssociation(
#			user = user,
#			identifier =fb_profile['id'],
#			token=access_key)
#			fb_record.save()
			html_content = render_to_string('meas/new_user_fb.html', {'user':user}) 
			text_content = strip_tags(html_content)
			subject, from_email, to = 'Adımsayar Üyelik Bilgileriniz.', 'adimsayarbilgi@gmail.com', email
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			return True

					

def process_device(user, device_id, manufacturer, model, product):
	error = False;
	if (product == ""):
		product = "null"

	if (model == ""):
		model = "null"

	if (manufacturer == ""):
		manufacturer = "null"

	#TODO what if fails
#try:
	device, created = Device2.objects.get_or_create(device_id=device_id, user=user)
	if (created):
		if manufacturer != "null":
			manufacturer, created = Manufacturer.objects.get_or_create(name=manufacturer)
			device.manufacturer = manufacturer
		if product != "null":
			product,created = Product.objects.get_or_create(name=product)
			device.product = product
		if model != "null":
			model,created = Model.objects.get_or_create(name=model, manufacturer=manufacturer)
			device.model = model
		device.save()
		return error, device
#except:
#		error = True;
#		return error, None
#
		#print "created device_id="+device.device_id+" model="+str(device.model)+" product="+str(device.product)+" manufacturer="+str(device.manufacturer)+" user="+user.email
		#device.swversion = tmp_swversion
		#device.appversion = tmp_appversion
#		if (device.swversion != tmp_swversion):
#			device.swversion = tmp_swversion
#		if (device.appversion != tmp_appversion):
#			device.appversion = tmp_appversion	
#	else:
#		TODO update swversion...
#		return device
#	device.save()
	return error, device


def process_incoming_step(request, email, steps, hour, device_id,  access_key, access_md5, height, weight,age,gender,manufacturer,model,product):
	user = User.objects.get(email=email)
	now = datetime.now()
	lastday= now + timedelta(days=1)
	if 0<=int(hour)<=23:
		date =datetime(now.year, now.month, now.day, int(hour), now.minute, now.second, now.microsecond, now.tzinfo)
	else:
		return False, "hour"

	error, device = process_device(user, device_id, manufacturer, model, product)
	if (error):
		return error, "process_device"

	steps_all = Step.objects.filter(date_time__gt=now.strftime("%Y-%m-%d"), date_time__lt=lastday.strftime("%Y-%m-%d"),user=user)

	if (steps_all):	
		counter = 0
		total = 0
		for st in steps_all:
			steps_today=st.steps
			counter += 1
			if (counter==1):
				steps_list=steps_today.split(',')
				steps_list[int(hour)]=str(steps)
				steps_new_record=",".join(steps_list)	
			else:
				return False, "steps"
	else:
		total = int(steps)
		steps_list = ['0']*24
		steps_list[int(hour)]=str(steps)
		steps_new_record=",".join(steps_list)	
		new_meas = Step(user=user, device2=device)
		new_meas.steps = steps_new_record
		new_meas.total = total
		new_meas.date_time = date
		new_meas.steps2 = ""
		new_meas.save()

	if cache.get('grand_steps'):
		cache.incr('grand_steps', int(steps))
		statistics_update=Statistics.objects.filter()
		statistics_update.update(total_steps=cache.get('grand_steps'))
	else:
		steps_grand = Step.objects.all()
		steps_total_all = 0
		for t in steps_grand:
			steps_total_all +=int(t.total)
		cache.set('grand_steps', int(steps_total_all), 60*60*24*15)			
		statistics_steps=Statistics.objects.filter()
		if(statistics_steps):
			statistics_steps.update(total_steps=steps_total_all)
		else:
			statistics_save=Statistics(stat_time = datetime.now(),total_steps = steps_total_all)
			statistics_save.save()
	for i in steps_list:
		total +=int(i) 
	
	calories = "%0.2f" % float(int(total)*0.05)
	#steps_all.update(date_time=date,steps =steps_new_record,total=total,calories=calories)
	for s in steps_all:
		s.date_time = date
		s.steps = steps_new_record
		s.total = total
		s.calories = calories
		s.steps2 = ""
		s.save()
	return True, "OK"


def user_control_gmail(request,email,height,weight,age,gender):
	try:			
	    user = User.objects.get(email=email)
	    profile = Profile.objects.get(user=user)
	    if (profile.height==height and profile.weight==weight and profile.age==age and profile.gender==gender):
                return True
 	    else:
                try:
		    profile = Profile.objects.filter(user=user)
	 	    profile.update(height=height,weight=weight,age=age,gender=gender, ip_addr=get_client_ip(request))
                except:
                    pass
		return True	

	except:
	    random_pass = str(random.randint(100000, 999999))
	    user = User(username=email, email=email)
	    user.set_password(random_pass)
	    user.save()
	    profile, created = Profile.objects.get_or_create(user=user)
	    profile= Profile.objects.filter(pk=profile.id)
	    profile.update(height=height,weight=weight,age=age,gender=gender, ip_addr=get_client_ip(request))
	    html_content = render_to_string('meas/new_user_email.html', {'user':user,'random_pass':random_pass}) 
	    text_content = strip_tags(html_content)
	    subject, from_email, to = 'Adımsayar Üyelik Bilgileriniz.', 'adimsayarbilgi@gmail.com', email
	    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	    msg.attach_alternative(html_content, "text/html")
	    msg.send()
	    return True

#	return HttpResponse('OK')
def http_get_sec(request):
	return HttpResponse('OK')
	try:
		if cache.get('http_get_count') !=None:
			cache.incr('http_get_count', 1 )
			statistics_update=Statistics.objects.filter()
			statistics_update.update(total_get=cache.get('http_get_count'))
		else:
			statistics=Statistics.objects.filter()
			cache.set('http_get_count', int(statistics[0].total_get), 60*60*24*15)
		email = request.GET.get('email', '')
		steps = request.GET.get('steps', '')
		hour = request.GET.get('hour', '')
		weight = request.GET.get('weight', '')
		gender = request.GET.get('gender', '')
		age = request.GET.get('age', '')
		height = request.GET.get('height', '')
		device_id = request.GET.get('device_id', '')
		access_md5 = request.GET.get('token', '')
		access_key = request.GET.get('access_key', '')
		login_type = request.GET.get('login_type', '')
		manufacturer = request.GET.get('manufacturer', '')
		model = request.GET.get('model', '')
		product = request.GET.get('product', '')

		#return HttpResponse(get_client_ip(request))

		#TODO we can also use regex here
		if (len(email)<7) or (email=="null"):
			cause = "email"
			raise invalidRequest

		if (len(access_md5)<30):
			cause = "token"
			raise invalidRequest

		if not((login_type == "fb") or (login_type == "email")):
			cause = "login_type"
			raise invalidRequest

		if (login_type == "fb"):
			if ((len(access_key) < 10) or (access_key == "null")):
				cause = "access_key"
				raise invalidRequest

		if (len(device_id)<10):
			cause = "device_id"
			raise invalidRequest

		if not(access_control(access_md5,device_id,request)):
			cause = "access_control"
			raise invalidRequest

		#TODO set these variables to none if they are null or doesnt exist
		# height, weight, age, gender, manufacturer, model, product

		if (login_type == "fb"):
			user_check=user_control_fb(request,access_key,email,height,weight,age,gender)
		elif (login_type == "email"):
			user_check=user_control_gmail(request,email,height,weight,age,gender)
		else:
			cause = "unknown_error"
			raise invalidRequest

		#TODO steps and hour?

		result,cause=process_incoming_step(request, email, steps, hour, device_id, access_key, 
					access_md5, height, weight,age,gender,manufacturer,model,product)

		if (result==True):
			#req = HttpReq(req = request.build_absolute_uri(), resp="OK")
			#req.save()
			return HttpResponse('OK')
		else:
			req = HttpReq(req = request.build_absolute_uri(), resp="FAIL", cause=cause)
			req.save()
			return HttpResponse('FAIL')
	except invalidRequest:
		if not(cause == "email"):
			req = HttpReq(req = request.build_absolute_uri(), resp="FAIL", cause=cause)
			req.save()
		return HttpResponse("FAIL:invalid request")


def get_atom(request):
	email = request.GET.get('email', '')
	access = True
	login = True
	if (login == True and access == True):
		user = User.objects.filter(email__exact = email)
		profile = Profile.objects.filter(user=user[0])
		diet = profile[0].diet
		atoms = Atom.objects.filter(diet=diet)
		response_data = serializers.serialize('json', atoms)
		return HttpResponse(response_data, mimetype='application/json')
	else:
		return HttpResponse('FAIL')
	return HttpResponse(request.user.email)

def http_get(request):
	email = request.GET.get('email', '')
	steps = request.GET.get('steps', '')
	hour = request.GET.get('hour', '')
	weight = request.GET.get('weight', '')
	gender = request.GET.get('gender', '')
	age = request.GET.get('age', '')
	height = request.GET.get('height', '')
	device_id = request.GET.get('device_id', '')
	access_md5 = request.GET.get('token', '')
	access_key = request.GET.get('access_key', '')
	return HttpResponse('OK')


from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from core.models import Profile
from content.models import Content
from django.template import RequestContext, loader
from badges.models import Badge, BadgeToUser
from django.core import serializers
from django.utils import simplejson
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
import random

def dont_mail(request):
	email = request.GET.get('email', '')
	if not (email):
		return HttpResponseRedirect('/')
	content= Content.objects.get(page='dont_send')
	user = User.objects.get(email=email)
	mail_type=request.GET.get('mail_type','')
	profile = Profile.objects.filter(user=user)
	if mail_type == "weight_update":
		profile.update(send_mail_weight_update=False)
	elif mail_type == "weekly":
		profile.update(send_mail_weekly=False)
	elif mail_type == "won_badge":
		profile.update(send_mail_won_badge=False)
	return render_to_response('profile/dont_mail.html',{'user':user, 'content':content, 'mail_type':mail_type}, context_instance=RequestContext(request))

def test_lang(request):
	return HttpResponse(request.LANGUAGE_CODE)

def user_delete(request):
	email = request.GET.get('email', '')
	if not (email):
		return HttpResponseRedirect('/')
	try:
		content= Content.objects.get(page='user_deleted')
		user = User.objects.get(email=email)
		user.is_active=False
		user.save()
		return render_to_response('profile/user_deleted.html',{'user':user,'content':content}, context_instance=RequestContext(request))
	except:
		return HttpResponseRedirect('/')


def authorize_user(request):
    resp = dict()
    try:
        email = request.POST.get('email', '')
        password = request.POST.get('key', '')
        user = User.objects.get(email=email)
        result = authenticate(username=user.username,password=password)
        if result is not None:
            resp['status'] = "OK"
        else:
            resp['status'] = "FAIL"
            resp['error'] = "user not found"
    except Exception,err:
        resp['status'] = "FAIL"
        resp['error'] = str(err)
    finally:
        response = simplejson.dumps(resp)
        return HttpResponse(response, mimetype='application/json')


def register_email_user(request):
    resp = dict()
    try:
        email = request.POST.get('email', '')
        key = request.POST.get('key', '')
        key_int = int(key)
        if ((key_int - 33900) != len(email)):
            raise Exception("key_error")
        random_pass = str(random.randint(100000, 999999))
        user,created = User.objects.get_or_create(username=email, email=email)
        user.set_password(random_pass)
        user.save()
        profile, created = Profile.objects.get_or_create(user=user)
        profile= Profile.objects.filter(pk=profile.id)
        profile.update()
        html_content = render_to_string('meas/new_user_email.html', {'user':user,'random_pass':random_pass}) 
        text_content = strip_tags(html_content)
        subject, from_email, to = 'Adimsayar Uyelik Bilgileriniz.', 'adimsayarbilgi@gmail.com', email
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        resp['status'] = "OK"
    except Exception, err:
        resp['status'] = "FAIL"
        resp['error'] = str(err)
    finally:
        response = simplejson.dumps(resp)
        return HttpResponse(response, mimetype='application/json')

def reset_password_email(request):
    resp = dict()
    try:
        email = request.POST.get('email', '')
        key = request.POST.get('key', '')
        key_int = int(key)
        if ((key_int - 33900) != len(email)):
            raise Exception("key_error")
        random_pass = str(random.randint(100000, 999999))
        user = User.objects.get(email=email)
        user.set_password(random_pass)
        user.save()
        profile, created = Profile.objects.get_or_create(user=user)
        profile= Profile.objects.filter(pk=profile.id)
        profile.update()
        html_content = render_to_string('meas/new_user_email.html', {'user':user,'random_pass':random_pass}) 
        text_content = strip_tags(html_content)
        subject, from_email, to = 'Adimsayar Uyelik Bilgileriniz.', 'adimsayarbilgi@gmail.com', email
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        resp['status'] = "OK"
    except Exception, err:
        resp['status'] = "FAIL"
        resp['error'] = str(err)
    finally:
        response = simplejson.dumps(resp)
        return HttpResponse(response, mimetype='application/json')

def my_badges(request):
    user = User.objects.get(id=request.user.id)
    badge_to_user = BadgeToUser.objects.filter(user=user)
    return render_to_response('badges/my_badges.html',
            {'user':user,'badge_to_user':badge_to_user}, 
            context_instance=RequestContext(request))
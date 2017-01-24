# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.context import RequestContext
from body_info.models import BodyInfo
from device2.models import Device2, Manufacturer, Model, Product
from core.models import Profile
from meas.views import steps_commit
from django.template.loader import render_to_string
import json
import random
import md5
import hashlib
import unicodedata
import os

def logit(msg):
    os.system("echo "+str(msg)+" >> /tmp/mobsynclog")

def process_device(user, device_id, manufacturer, model, product):
    if (product == ""):
        product = "null"

    if (model == ""):
        model = "null"

    if (manufacturer == ""):
        manufacturer = "null"

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
    return device, created


def reset_password_email(user):
    random_pass = str(random.randint(100000, 999999))
    html_content = render_to_string('meas/new_user_email.html', 
                        {'user':user,'random_pass':random_pass}) 
    text_content = strip_tags(html_content)
    subject, from_email, to = ('Adımsayar Üyelik Bilgileriniz.', 
                            'adimsayarbilgi@gmail.com', user.email)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def get_client_ip(request):
    logit("GETCLIENT_IP")
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def config_sync(request):
    logit("started")
    resp = dict()
    resp['result'] = "OK"
    resp['error'] = "None"
    json_data = json.dumps(resp)
    return HttpResponse(json_data, mimetype="application/json")
    try:
        if not request.POST:
            raise Exception('Protocol Error')

        email = request.POST.get('email', None)
        device_id = request.POST.get('device_id', None)
        token = request.POST.get('token', None)
        logit("email="+str(email)+" device_id="+str(device_id))
        if not (email and device_id and token):
            raise Exception('Credentials')

        secret = email+'|dex|'+str(len(email))
        token_gen = hashlib.md5(secret).hexdigest()
        if (token_gen != token):
            raise Exception('Credentials2')

        #TODO:generate a username for whose email is more than 30 chars
        user_created = False
        tmp_count = User.objects.filter(email=email).count()
        if (tmp_count == 1):
            user = User.objects.get(email=email)
        elif (tmp_count == 0):
            indx = email.index('@')
            username = email[0:indx]
            user = User(username=username, email=email)
            user.save()
            user_created = True
        elif (tmp_count > 1):
            raise Exception("multiple account for user name")

        prof, profile_created  = Profile.objects.get_or_create(user=user)
        if (profile_created):
            prof.save()

        #TODO save ip
        #TODO save location

        model = request.POST.get('model', None)
        product = request.POST.get('product', None)
        manufacturer = request.POST.get('manufacturer', None)
        device, device_created = process_device(user=user, device_id=device_id, 
                         product=product, model=model, manufacturer=manufacturer)

        request_password = request.POST.get('request_password', None)
        if (request_password or user_created):
            reset_password_email(user)
            #TODO send mail

        for key, value in request.POST.iteritems():
            if ((key[0] == 's') and (key[1] == 't')):
                am_key = key
                am_key = am_key.replace('st','am')
                am_value = request.POST.get(am_key, "")
                today, retval = steps_commit(user, device, key, value, am_value)
                if (retval >= 0):
                    if not (today):
                        update_vars[key] = ""
                        update_vars[am_key] = ""
                else:
                    resp['result'] = "FAIL"

        #here we may check RemoteConfigs if user needs update
        #what is the maximum size of a key,value?
        ads_enabled = request.POST.get('ads_enabled', 'no')
        if (ads_enabled == 'no'):
            update_vars['ads_enabled'] = "yes"
            update_vars['ad_position'] = "bottom"
            logit("ADS_ENABLED")

        config_changed = request.POST.get('config_changed', 'no')
        logit("DONE0:"+config_changed)
        if (config_changed == 'yes'):
            gender = request.POST.get('gender', "")
            age = request.POST.get('age', None)
            height = request.POST.get('height', None)
            weight = request.POST.get('weight', None)
            lifestyle = request.POST.get('lifestyle', None)
            sensivity = request.POST.get('sensivity', None)
            mode = request.POST.get('mode', None)

            if (gender or age or weight or height or lifestyle):
                prof.gender = gender
                prof.age = age
                prof.weight = weight
                prof.height = height
                prof.lifestyle = lifestyle
                logit("profipaddr="+str(prof.ip_addr))
                if not (prof.ip_addr):
                    prof.ip_addr = get_client_ip(request)
                try:
                    logit('YES4')
                    prof.save()
                    logit('YES5')
                except Exception,err:
                    logit("PROF-ERROR"+str(err))
                    pass
                #This is a workaround:Profile doesnt create bi if it is newly created
                if (profile_created) and age and weight and height and gender:
                    bi = BodyInfo(gender=gender, lifestyle=lifestyle,
                                  weight=weight, height=height, age=age)
                    try:
                        logit('YES6')
                        bi.save()
                        logit('YES7')
                    except Exception,err:
                        logit("BIERROR"+str(err))
                        pass

            if sensivity:
                device.sensivity = sensivity

            if mode:
                device.mode = mode
            device.save()
            update_vars['config_changed'] = ''

    except Exception,err:
        resp['result'] = 'FAIL'
        resp['error'] = str(err)
        logit("EXCEPTION:"+resp['error'])
        #logit(str(err)+":"+device_id+","+email+","+token)
        if (str(err) == 'Credentials'):
            update_vars['device_id'] = ""
    finally:
        logit("FINALLY:"+resp['result']+",err="+resp['error'])
        resp['update'] = update_vars
        json_data = json.dumps(resp)
        return HttpResponse(json_data, mimetype="application/json")

def latest_version(request):
    resp = dict()
    resp['result'] = ""

    if not request.POST:
        resp['result'] = "FAIL"
        resp['error'] = "No data given"

    platform = request.POST.get('platform', None)

    if not platform:
        resp['result'] = "FAIL"
        resp['error'] = "which platform?"

    if platform == "android":
        resp['result'] = "1.5.0"
    else:
        resp['result'] = "1.3.0"

    json_data = json.dumps(resp)
    return HttpResponse(json_data, mimetype="application/json")







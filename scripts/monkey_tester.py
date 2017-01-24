# -*- coding: utf-8 -*-
import os
import sys

heads, tail = os.path.split(os.path.dirname(os.path.abspath(__file__)))
site_root, project_dir_name = os.path.split(heads)
sys.path.append(heads)

os.environ['PROJECT_DIR_NAME'] = project_dir_name
os.environ['DJANGO_SETTINGS_MODULE'] = project_dir_name + '.settings'
os.environ['OVERLOAD_SITE'] = 'adimsayar'
os.environ['SITE_ROOT'] = os.path.dirname(__file__)


from django.core.management import setup_environ
import settings

setup_environ(settings)
DEBUG = False

#keep this for render_to_string unicode errors
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from datetime import datetime,timedelta
from core.models import Profile
from body_info.models import BodyInfo
from statistics.models import DailyStatistics
from statistics.models import AgeVsUser
from statistics.models import BmiVsUser
from statistics.models import AvgDailyStep
from django.core.cache import cache
from meas.models import *
from meas.views import get_weekly_steps
import md5, hashlib, urllib
from random import randrange
import time

ADMIN_EMAIL = "ozkolonur@gmail.com"

# howto get long-lived access token ?
# https://graph.facebook.com/oauth/access_token?client_id=210050799065722&client_secret=6c5ca248f1e45c226b8778b5f651ffe3&grant_type=fb_exchange_token&fb_exchange_token=AAACZCCkNDWnoBANNogzrzCLag7Nac58jWtW3CyCCYhDpYlvw8vGQm19s0ZC6zMIN0hWomFiwC9p8zFnuS8X05vy3rLqDCY639bkaO1bTjaOFyeTfhc

#default variables
main_url="http://www.adimsayar.com/mining_platform/http_get_sec/?"
#biz:access_key="AAACGDrKtV8oBALFYVZCmZCooTpv4JzFiJ36fMumGByfjFo8IsdvLj6SYD2nZCEXdMO5PMEVRmxCTCJgmlNgkAddggN0sksEGklebRVVuMKaZAuhGfc0r"
#access_key="AAACZCCkNDWnoBAGT2QvriH6fna55Lt5r3JqNtJNcWbA1PWxTY2mQcBtwJctjkRfHZCOhJMLPMtBoGdJpZBLZAWqSXZBjXRfWV88wbpm9AjgZDZD"
#access_key="AAACZCCkNDWnoBAEZAS1R087Iqb6VE8wVQvzDbRZCMrn1yLAbaq2ZA97EJKjYo7qZC2TaN9rk0f8WcoZCWKmKfpMRW9ZCYYI5o5NlUxZAM7HzqgZDZD"
access_key="AAACZCCkNDWnoBAPEZAZAAqBZAolIZBIsEuse5V26XoZBNkaiHk1Me4kfwMqGDJBZC78nDIjb29ndlWWFQaE8UZCvPgWlsPdlOzqUiQFhaCvXLQZDZD"
email="adimsayarmonk@gmail.com"
device_id="fffffffe-a0e0-17d4-4349-5aae2fce6653"
steps="205"
hour="12"
gender="male"
age="28"
height="178"
weight="78"
login_type="fb"
manufacturer="HUAWEI"
model="Turkcell T20"
version="13"
product="U8650-1"
token="69e8b12fe9e555831d4da3429e72cac"

def test1():
    height = str(randrange(130, 210))
    weight = str(randrange(30, 180))
    age = str(randrange(4, 100))
    steps = str(randrange(1, 4000))
    hour = str(randrange(0, 22))
    url = main_url
    url += "email="+ email + "&"
    url += "device_id="+ device_id + "&"
    url += "hour="+ hour + "&"
    url += "steps="+ steps + "&"
    url += "gender="+ gender + "&"
    url += "age="+ age + "&"
    url += "height="+ height + "&"
    url += "weight="+ weight + "&"
    url += "login_type="+ login_type + "&"
    url += "manufacturer="+ urllib.quote(manufacturer) + "&"
    url += "model="+ urllib.quote(model) + "&"
    url += "version="+ version + "&"
    url += "product="+ urllib.quote(product) + "&"
    url += "access_key="+ access_key

    secret_key = "erdex|%04d|" % len(url) + device_id
    token =hashlib.md5(secret_key).hexdigest()
    url += "&" + "token="+ token
    print "Test url:" + url
    result = urllib.urlopen(url)

    res = result.read()
    if "FAIL" in res:
        print "1A Failed"
        log_to_mail(ADMIN_EMAIL, 'Monkey Tester', 'Step 1A failed:' + url)
    else:
        print "1A Successful"

    user = User.objects.get(email=email)
    profile = Profile.objects.get(user=user)
    if (str(profile.height) == height and str(profile.weight) == weight and 
        str(profile.age) == age):
        print "1B Successful"
    else:
        print "1B Failed"
        log_to_mail(ADMIN_EMAIL, 'Monkey Tester', 'Step 1B failed:'+url)

    step_latest = Step.objects.filter(user=user).order_by('-date_time')[0]
    if steps in step_latest.steps:
        steps_str = step_latest.steps
        steps_list = steps_str.split(',')
        if steps_list.index(str(steps)) == int(hour):
            print "1C Successful"
        else:
            print "1C Failed"
            log_to_mail(ADMIN_EMAIL, 'Monkey Tester', 'Step 1C failed:'+url)
    else:
        print "1C Failed"
        log_to_mail(ADMIN_EMAIL, 'Monkey Tester', 'Step 1C failed:'+url)

    device = Device2.objects.get(user=user)
    if (device.product.name == product and device.manufacturer.name == manufacturer and 
        device.model.name == model):
        print "1D Successful"
    else:
        print "1D Failed"
        log_to_mail(ADMIN_EMAIL, 'Monkey Tester', 'Step 1D failed:'+url)

    time.sleep(3)

    #update some variables and check if they are updated on server
    steps_int = int(steps)
    steps_int += 100
    steps = str(steps_int)

    hour_int = int(hour)
    hour_int += 1
    hour = str(hour_int)

    weight_int = int(weight)
    weight_int += 1
    weight = str(weight_int)

    url = main_url
    url += "email="+ email + "&"
    url += "device_id="+ device_id + "&"
    url += "hour="+ hour + "&"
    url += "steps="+ steps + "&"
    url += "gender="+ gender + "&"
    url += "age="+ age + "&"
    url += "height="+ height + "&"
    url += "weight="+ weight + "&"
    url += "login_type="+ login_type + "&"
    url += "manufacturer="+ urllib.quote(manufacturer) + "&"
    url += "model="+ urllib.quote(model) + "&"
    url += "version="+ version + "&"
    url += "product="+ urllib.quote(product) + "&"
    url += "access_key="+ access_key

    secret_key = "erdex|%04d|" % len(url) + device_id
    token =hashlib.md5(secret_key).hexdigest()
    url += "&" + "token="+ token
    print "Test url:" + url
    result = urllib.urlopen(url)

    res = result.read()
    if "FAIL" in res:
        print "1E Failed"
        log_to_mail(ADMIN_EMAIL, 'Monkey Tester', 'Step 1E failed:' + url)
    else:
        print "1E Successful"

    user = User.objects.get(email=email)
    profile = Profile.objects.get(user=user)
    if (str(profile.height) == height and str(profile.weight) == weight and 
        str(profile.age) == age):
        print "1F Successful"
    else:
        print "1F Failed"
        log_to_mail(ADMIN_EMAIL, 'Monkey Tester', 'Step 1F failed:'+url)

    step_latest = Step.objects.filter(user=user).order_by('-date_time')[0]
    if steps in step_latest.steps:
        steps_str = step_latest.steps
        steps_list = steps_str.split(',')
        if steps_list.index(str(steps)) == int(hour):
            print "1G Successful"
        else:
            print "1G Failed"
            log_to_mail(ADMIN_EMAIL, 'Monkey Tester', 'Step 1G failed:'+url)
    else:
        print "1F Failed"
        log_to_mail(ADMIN_EMAIL, 'Monkey Tester', 'Step 1G failed:'+url)

    user.delete()


def log_to_mail(email, subject, message):
    to = [email]
    from_email = 'adimsayarbilgi@gmail.com'
    msg = EmailMultiAlternatives(subject, message, from_email, to)
    msg.send()


try:
    test1()
except Exception, err:
    log_to_mail(ADMIN_EMAIL, 'Monkey Tester', 'Exception:'+str(err))

sys.exit()

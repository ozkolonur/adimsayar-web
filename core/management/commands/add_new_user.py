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
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from body_info.models import BodyInfo
from datetime import datetime, timedelta



ADMIN_EMAIL = "ozkolonur@gmail.com"

# howto get long-lived access token ?
# https://graph.facebook.com/oauth/access_token?client_id=210050799065722&client_secret=6c5ca248f1e45c226b8778b5f651ffe3&grant_type=fb_exchange_token&fb_exchange_token=AAACZCCkNDWnoBANNogzrzCLag7Nac58jWtW3CyCCYhDpYlvw8vGQm19s0ZC6zMIN0hWomFiwC9p8zFnuS8X05vy3rLqDCY639bkaO1bTjaOFyeTfhc

#default variables
main_url="http://www.adimsayar.com/mining_platform/http_get_sec/?"
#biz:access_key="AAACGDrKtV8oBALFYVZCmZCooTpv4JzFiJ36fMumGByfjFo8IsdvLj6SYD2nZCEXdMO5PMEVRmxCTCJgmlNgkAddggN0sksEGklebRVVuMKaZAuhGfc0r"
access_key="AAACZCCkNDWnoBAGT2QvriH6fna55Lt5r3JqNtJNcWbA1PWxTY2mQcBtwJctjkRfHZCOhJMLPMtBoGdJpZBLZAWqSXZBjXRfWV88wbpm9AjgZDZD"
device_id="fffffffe-e0e0-17d4-4349-5aae2fce6653"
steps="205"
hour="12"
gender="male"
age="28"
height="178"
weight="78"
login_type="email"
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
    global device_id
    device_id = device_id + "-" + str(randrange(0,1000000))
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
        print "Registration Failed"
    else:
        print "Registration Successful"


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'For every user calculates hourly step\
             stats and keep it in HourlyStepAvg table'

    def handle(self, *args, **options):
        global email
        email = args[0]
        test1()





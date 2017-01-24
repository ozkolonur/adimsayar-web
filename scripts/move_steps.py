# -*- coding: utf-8 -*-
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
from statistics.models import DailyStatistics
from django.core.cache import cache
from meas.models import *
import time, cgi, urllib, urllib2
from django.http import HttpResponse
from core.models import Location, Country, City, Isp
from device2.models import Device2, Product, Model, Manufacturer

steps = Step.objects.all()
for step in steps:
	try:
		if len(step.device2.device_id) > 0:
			continue
		user = step.user
		device2 = Device2.objects.filter(user=user)
		step.device2 = device2[0]
		#print "device=" + device.device_id + "user =" + user.email
		step.save()
	except:
		print "exception  user :" + user.email
		continue

#steps = Step.objects.all()
#for step in steps:
#	user = step.user
#	if user.email == "kubrasarall@hotmail.com":
#		continue
#	device2 = Device2.objects.get(user=user)
#	step.device2 = device2
#	print "device=" + device2.device_id + "user =" + user.email
#	#step.save()

#steps = Step.objects.all()
#for step in steps:
#	user = step.user
#	print len(step.device2.device_id)
	#if step.device2 == "":
	#	print "step device none"

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
from statistics.models import DailyStatistics
from django.core.cache import cache
from meas.models import *
import time, cgi, urllib, urllib2
from django.http import HttpResponse
from core.models import Location, Country, City, Isp, Profile
from device2.models import Device2, Product, Model, Manufacturer
from body_info.models import BodyInfo

def create_body_info():
	#print ' === HEIGHT === '
	counter = 0;
	ex_counter = 0;
	users = User.objects.all()
	for user in users:
		try:
			profile = Profile.objects.get(user=user)
			#print ""+ str(profile.age)
			if profile.weight and profile.weight < 300 and profile.weight > 20 and profile.height and profile.height > 40 and profile.height < 250 and profile.age and profile.age < 150 and profile.age > 6:
#				print "creating body_info="+user.email
				counter += 1
				body_info = BodyInfo(user=user, age=profile.age, weight=profile.weight, height=profile.height, gender=profile.gender)
				body_info.save()
		except Exception, err:
			print "EXCEPTION:"+user.email
			ex_counter += 1
			print err
	print "ex_counter=" + str(ex_counter)
	print "counter=" + str(counter)
	
			

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

#create_body_info()

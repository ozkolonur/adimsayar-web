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

sys.exit()

steps = Step.objects.all()
for step in steps:
	try:
		device = step.device
		user = step.user
		#print "device_id="+device.device_id+" model="+device.model+" product="+device.product+" manufacturer="+device.manufacturer+" user="+user.email
		tmp_product = device.product
		tmp_model = device.model
		tmp_manufacturer = device.manufacturer
		tmp_device_id = device.device_id
		tmp_swversion = None
		tmp_appversion = None
		if device.product == "":
			tmp_product = "null"
		if device.manufacturer == "":
			tmp_manufacturer = "null"
		if device.model == "":
			tmp_model = "null"
		if device.model == "bpm-111":
			tmp_model = "null"
		if device.product is None:
			tmp_product = "null"
		if device.manufacturer is None:
			tmp_manufacturer = "null"
		if device.model is None:
			tmp_model = "null"
		if tmp_model.find("Android-") >= 0:
			tmp_model = "null"
		if tmp_product != "null":
			product,created = Product.objects.get_or_create(name=tmp_product)
		if tmp_manufacturer != "null":
			manufacturer, created = Manufacturer.objects.get_or_create(name=tmp_manufacturer)
		if tmp_model != "null":
			model,created = Model.objects.get_or_create(name=tmp_model, manufacturer=manufacturer)
	except:
		print 'exception :'+ tmp_device_id + " user :" + user.email
		continue
	try:
		device, created = Device2.objects.get_or_create(device_id=tmp_device_id, user=user)
	except:
		print 'exception :'+ tmp_device_id + " user :" + user.email
		continue
	if (created):
		try:
			#print "created device_id="+device.device_id+" model="+str(device.model)+" product="+str(device.product)+" manufacturer="+str(device.manufacturer)+" user="+user.email
			device.swversion = tmp_swversion
			device.appversion = tmp_appversion
			if tmp_product != "null":
				device.product = product
			if tmp_model != "null":
				device.model = model
			if tmp_manufacturer != "null":
				device.manufacturer = manufacturer
			device.device_id = tmp_device_id
			device.user = user
#		if (device.swversion != tmp_swversion):
#			device.swversion = tmp_swversion
#		if (device.appversion != tmp_appversion):
#			device.appversion = tmp_appversion	
		except:
			print 'exception :'+ tmp_device_id + " user :" + user.email
			pass
	#device.save()
	step.device = device
			
#	return HttpResponse("OK")
#users = User.objects.all()
#for user in users:
#	if user.email == 'admin@admin.com':
#		continue
#	print 'processing:' + user.email
#	profile = Profile.objects.get(user=user)
#	print 'ip_addr was:' + profile.ip_addr + ' len=' + str(len(profile.ip_addr)) 
#	if (len(profile.ip_addr) > 5):
#		update_user_location(profile)
#		print 'location updated: ' + user.email
#	else:
#		continue


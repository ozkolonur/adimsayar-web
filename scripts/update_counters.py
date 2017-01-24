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
from core.models import Location, Country, City, Isp
from device2.models import Device2, Product, Model, Manufacturer
# Create your views here.

countries = Country.objects.all()
for country in countries:
	country.cnt = 0;
	country.save()

cities = City.objects.all()
for city in cities:
	city.cnt = 0;
	city.save()

isps = Isp.objects.all()
for isp in isps:
	isp.cnt = 0;
	isp.save()

users = User.objects.all()
for user in users:
	try:
		profile = Profile.objects.get(user=user)
	except:
		continue
	if profile.user_location:
		print user.email
		country = profile.user_location.country
		country.cnt = country.cnt + 1
		country.save()
		city = profile.user_location.city
		city.cnt = city.cnt + 1
		city.save()
		isp = profile.isp
		isp.cnt = isp.cnt + 1
		isp.save()

manufacturers = Manufacturer.objects.all()
for manufacturer in manufacturers:
	manufacturer.cnt = 0;
	manufacturer.save()

models = Model.objects.all()
for model in models:
	model.cnt = 0;
	model.save()

products = Product.objects.all()
for product in products:
	product.cnt = 0;
	product.save()

devices = Device2.objects.all()
for device in devices:
	print device.device_id
	if device.manufacturer:
		manufacturer = device.manufacturer
		manufacturer.cnt = manufacturer.cnt + 1
		manufacturer.save()
	if device.model:
		model = device.model
		model.cnt = model.cnt + 1
		model.save()
	if device.product:
		product = device.product
		product.cnt = product.cnt + 1
		product.save()





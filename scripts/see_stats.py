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
import gc
import sys

def arithmeticMean(int_list):
	total = 0 
	for itr in int_list:
		total += itr
	#print 'total=' + str(total)
	#print 'len(int_list)=' + str(len(int_list))
	#print 'mean=' + str(total/len(int_list))
	return "%0.2f" % float(total/(len(int_list) * 1.00))

def getAverageAge():
	print ' === AGE === '
	girls_age_list = []
	boys_age_list = []
	profiles = Profile.objects.all()
	for profile in profiles:
		if profile.age and profile.age < 120:
			if profile.gender == 'female':
				girls_age_list.append(int(profile.age))
			elif profile.gender == 'male':
				boys_age_list.append(int(profile.age))
	print 'GIRLS average ='+arithmeticMean(girls_age_list)
	print 'BOYS average ='+arithmeticMean(boys_age_list)
	print 'DONE.'

def getAverageWeight(age, height):
	print ' === WEIGHT === '
	girls_weight_list = []
	boys_weight_list = []
	profiles = Profile.objects.all()
	for profile in profiles:
		if profile.weight and profile.weight < 300 and profile.weight > 20 and profile.age == age and (profile.height - height < 1):
			if profile.gender == 'female':
				girls_weight_list.append(int(profile.weight))
			elif profile.gender == 'male':
				boys_weight_list.append(int(profile.weight))
	print 'GIRLS average='+arithmeticMean(girls_weight_list)
	print 'BOYS average='+arithmeticMean(boys_weight_list)
	print 'DONE.'

def getAverageHeight(age):
	print ' === HEIGHT === '
	girls_height_list = []
	boys_height_list = []
	profiles = Profile.objects.all()
	for profile in profiles:
		if profile.height and profile.height < 300 and profile.height > 50 and profile.age == age:
			if profile.gender == 'female':
				girls_height_list.append(int(profile.height))
			elif profile.gender == 'male':
				boys_height_list.append(int(profile.height))
	print 'GIRLS average='+arithmeticMean(girls_height_list)
	print 'BOYS average='+arithmeticMean(boys_height_list)
	print 'DONE.'


def updateAgeVsUser():
	print ' === AGE x NUM_OF_USERS === '
	girls_age_list = dict.fromkeys(range(7,120))
	for itr in girls_age_list:
		girls_age_list[itr]=0;
	boys_age_list = dict.fromkeys(range(7,120))
	for itr in boys_age_list:
		boys_age_list[itr]=0;
	users_age_list = dict.fromkeys(range(7,120))
	for itr in users_age_list:
		users_age_list[itr]=0;
	profiles = Profile.objects.all()
	for profile in profiles:
		if profile.age and profile.age < 120 and profile.age > 6:
			if profile.gender == 'female':
				girls_age_list[profile.age] += 1;
				users_age_list[profile.age] += 1;
			elif profile.gender == 'male':
				boys_age_list[profile.age] += 1;
				users_age_list[profile.age] += 1;
			else:
				users_age_list[profile.age] += 1;
				print 'no gender -> age='+ str(profile.age) + " first_name="+ str(profile.firstname)
	for itr in range(7,120):
		ageVsUser, created = AgeVsUser.objects.get_or_create(age=itr)
		ageVsUser.num_of_boys = boys_age_list[itr]
		ageVsUser.num_of_girls = girls_age_list[itr]
		ageVsUser.num_of_users = users_age_list[itr]
		ageVsUser.save()
	print 'DONE.'

def drange(start, stop, step):
	r = start
	while r < stop:
		yield r
		r += step

def updateBmiVsUser():
	i0 = drange(0, 2, 0.01)
	users_bmi_list = dict.fromkeys(["%.2f" % x for x in i0])
	for itr in users_bmi_list:
		users_bmi_list[itr] = 0

	i0 = drange(0, 2, 0.01)
	girls_bmi_list = dict.fromkeys(["%.2f" % x for x in i0])
	for itr in girls_bmi_list:
		girls_bmi_list[itr] = 0

	i0 = drange(0, 2, 0.01)
	boys_bmi_list = dict.fromkeys(["%.2f" % x for x in i0])
	for itr in boys_bmi_list:
		boys_bmi_list[itr] = 0

	body_infos = BodyInfo.objects.all()
	for body_info in body_infos:
		prime = body_info.bmi_prime()
		if prime:
			users_bmi_list[prime] += 1
			if body_info.gender == 'female':
				girls_bmi_list[prime] += 1
			elif body_info.gender == 'male':
				boys_bmi_list[prime] += 1
			else:
				print "Gender not defined"
	print users_bmi_list
	print boys_bmi_list
	print girls_bmi_list
	i0 = drange(0, 2, 0.01)
	for itr in ["%.2f" % x for x in i0]:
		#bmi = format( (itr * 25), '.2f')
		#print "%.2f" % (float(itr) * 25)
		bmiVsUser, created = BmiVsUser.objects.get_or_create(bmi="%.2f" % (float(itr) * 25))
		bmiVsUser.num_of_boys = boys_bmi_list[itr]
		bmiVsUser.num_of_girls = girls_bmi_list[itr]
		bmiVsUser.num_of_users = users_bmi_list[itr]
		bmiVsUser.save()
	print 'OK.'


def getUserDevice(email):
	user = User.objects.get(email=email)
	device = Device2.objects.get(user=user)
	return "manufacturer="+ device.manufacturer.name +\
			 " model="+device.model.name+\
				" product="+device.product.name

def selectGirlsSteps(steps):
	girls_step_list = []
	for step in steps:
		try:
			profile = Profile.objects.get(user=step.user)
			if profile.gender == "female":
				girls_step_list.append(step)
		except Exception, err:
			#print err
			continue
	return girls_step_list

def selectBoysSteps(steps):
	boys_step_list = []
	for step in steps:
		try:
			profile = Profile.objects.get(user=step.user)
			if profile.gender == "male":
				boys_step_list.append(step)
		except Exception, err:
			#print err
			continue
	return boys_step_list

def getAverageDailyStep(steps):
	daily_average = long(0)
	total = long(0)
	for step in steps:
		total += step.total
	daily_average = total / len(steps)
	return daily_average

def getStepcountByWeekday(steps):
	days_weekday = dict.fromkeys(range(0,7))
	for itr in days_weekday:
		days_weekday[itr] = 0

	users_stepcount_weekday = dict.fromkeys(range(0,7))
	for itr in users_stepcount_weekday:
		users_stepcount_weekday[itr] = 0

	normalized_stepcount_weekday = dict.fromkeys(range(0,7))
	for itr in normalized_stepcount_weekday:
		normalized_stepcount_weekday[itr] = 0

	for step in steps:
		users_stepcount_weekday[step.date_time.weekday()] += step.total
		days_weekday[step.date_time.weekday()] +=1

	#we may have more monday than tuesday here so we need to normalize it
	for itr in range(0,7):
		normalized_stepcount_weekday[itr] = \
			users_stepcount_weekday[itr] / days_weekday[itr]
	print "days_weekday="+str(days_weekday)
	return normalized_stepcount_weekday

def getAverageStepCount():
	print ' === STEP === '
	girls_age_list = []
	boys_age_list = []
	user_count = 0
	steps = Step.objects.all()
	steps_safe_device = []
	for step in steps:
		try:
			if step.device2.product.name == "GT-I9100" and \
					step.device2.model.name == "GT-I9100":
				steps_safe_device.append(step)

			elif step.device2.product.name =="htc_marvel" and \
					step.device2.model.name =="HTC Wildfire S A510e":
				steps_safe_device.append(step)

			elif step.device2.product.name =="htc_shooteru" and \
					step.device2.model.name =="HTC EVO 3D X515m":
				steps_safe_device.append(step)

			elif step.device2.product.name =="htc_runnymede" and \
					step.device2.model.name =="HTC Sensation XL with Beats Audio X315e":
				steps_safe_device.append(step)

			elif step.device2.product.name =="MT11i_1255-2312" and \
					step.device2.model.name =="MT11i":
				steps_safe_device.append(step)

			elif step.device.product =="GT-I9100" and \
					step.device.model =="GT-I9100":
				steps_safe_device.append(step)

			elif step.device.product =="htc_marvel" and \
					step.device.model =="HTC Wildfire S A510e":
				steps_safe_device.append(step)

			elif step.device.product =="htc_shooteru" and \
					step.device.model =="HTC EVO 3D X515m":
				steps_safe_device.append(step)

			elif step.device.product =="htc_runnymede" and \
					step.device.model =="HTC Sensation XL with Beats Audio X315e":
				steps_safe_device.append(step)

			elif step.device.product =="MT11i_1255-2312" and \
					step.device.model =="MT11i":
				steps_safe_device.append(step)
			else:
				pass #may delete
		except:
			pass #may delete

	#this is used for testing
	#steps_safe_device = []
	#steps_safe_device = Step.objects.all()
	print "total steps (users) =" + str(len(steps_safe_device))
	#users_stepcount_weekday = getStepcountByWeekday(steps_safe_device)
	users_stepcount_average_daily = getAverageDailyStep(steps_safe_device)
	print "user_stepcount_average_daily="+str(users_stepcount_average_daily)

	steps_safe_device_girls = selectGirlsSteps(steps_safe_device)
	print "total steps (girls) =" + str(len(steps_safe_device_girls))
	#girls_stepcount_weekday = getStepcountByWeekday(steps_safe_device_girls)
	girls_stepcount_average_daily = getAverageDailyStep(steps_safe_device_girls)
	print "girls_stepcount_average_daily="+str(girls_stepcount_average_daily)

	steps_safe_device_boys = selectBoysSteps(steps_safe_device)
	print "total steps (boys) =" + str(len(steps_safe_device_boys))
	#boys_stepcount_weekday = getStepcountByWeekday(steps_safe_device_boys)
	boys_stepcount_average_daily = getAverageDailyStep(steps_safe_device_boys)
	print "boys_stepcount_average_daily="+str(boys_stepcount_average_daily)

	stat = AvgDailyStep()
	stat.girls_average = girls_stepcount_average_daily
	stat.boys_average = boys_stepcount_average_daily
	stat.users_average = users_stepcount_average_daily
	stat.save()

def getNumGender():
	numBoys = 0;
	numGirls = 0;
	numUnknown = 0;
	gc.collect()
	users = User.objects.all();
	for user in users:
	  try:
		print '.'
		profile = Profile.objects.get(user=user)
		if (profile.gender == "male"):
			numBoys += 1;
		elif (profile.gender == "female"):
			numGirls += 1;
		else:
			numUnknown += 1;
		del profile
	  except:
		continue;
	return str(numGirls), str(numBoys), str(numUnknown)

#girls, boys, unknown = getNumGender()
#print "numBoys="+boys
#print "numGirls="+girls
#print "numUnknown="+unknown

#getAverageAge()
#getAverageWeight(27, 178)
#getAverageHeight(27)

#this is tested, should be scheduled to cron
updateAgeVsUser()
updateBmiVsUser()
getAverageStepCount()











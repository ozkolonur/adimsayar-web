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
#import gdata.sample_util
from meas.models import *
from device2.models import Device2, Manufacturer

def createStat():
  yesterday = (datetime.today() - timedelta(1))
  stat,created = DailyStatistics.objects.get_or_create(stat_time = yesterday.strftime("%Y-%m-%d"))
  return stat
'''
def getDailyVisitsFromGoogle(date):
  email = 'ozkolonur@gmail.com'
  password = '********'
  """Inits DataFeedDemo."""
  SOURCE_APP_NAME = 'Google-dataFeedDemoPython-v2'
  my_client = gdata.analytics.client.AnalyticsClient(source=SOURCE_APP_NAME)
  try:
    gdata.sample_util.authorize_client(
        my_client,
        service=my_client.auth_service,
        source=SOURCE_APP_NAME,
        scopes=['https://www.google.com/analytics/feeds/'])
  except gdata.client.BadAuthentication:
    exit('Invalid user credentials given.')
  except gdata.client.Error:
    exit('Login Error')
    table_id = gdata.sample_util.get_param(
      name='table_id',
      prompt='Please enter your Google Analytics Table id (format ga:xxxx)')
    # DataFeedQuery simplifies constructing API queries and uri encodes params.
  data_query = gdata.analytics.client.DataFeedQuery({
      'ids': 'ga:52897390',
      'start-date': date,
      'end-date': date,
      'dimensions': 'ga:source,ga:medium',
      'metrics': 'ga:visits',
      'sort': '-ga:visits',
      'filters': 'ga:medium==referral',
      'max-results': '50'})
  feed = my_client.GetDataFeed(data_query)
  #print '\n-------- One Entry --------'
  entry = feed.entry[0]
  for met in entry.metric:
	return met.value
  #print 'ID      = ' + entry.id.text
  #for dim in entry.dimension:
  #	print 'Dimension Name  = ' + dim.name
  #	print 'Dimension Value = ' + dim.value
  #for met in entry.metric:
  #	print 'Metric Name     = ' + met.name
  #	print 'Metric Value    = ' + met.value
  #	print 'Metric Type     = ' + met.type
  #	print 'Metric CI       = ' + met.confidence_interval
   '''


def getTotalSteps():
	yesterday = (datetime.today() - timedelta(2))
	steps_grand = Step.objects.filter(date_time__gt = yesterday)
	steps_total_all = 0
	for t in steps_grand:
		steps_total_all +=int(t.total)
	return str(steps_total_all)

def getGrandTotalSteps():
	yesterday = (datetime.today() - timedelta(2))
	steps_grand = Step.objects.filter()
	steps_total_all = 0
	for t in steps_grand:
		steps_total_all +=int(t.total)
	return str(steps_total_all)


def getNumFbUsers():
	fbUsers = 0;
	yesterday = (datetime.today() - timedelta(2))
	users = User.objects.filter(date_joined__gt = yesterday);
	for user in users:
		try:
			fb_token = UserAssociation.objects.get(user=user)
			if (fb_token.token):
				fbUsers += 1;
		except:
		  continue;
	return str(fbUsers)

#number of users has sent meass more than three or more days
def getActiveUsers():
	activeUsers = 0;
	last5days = (datetime.today() - timedelta(5))
	users = User.objects.all();
	for user in users:
		step = Step.objects.filter(user=user, date_time__gt = last5days)
		if (step.count() > 2):
			activeUsers += 1;
	return str(activeUsers)


def getTotalUsers():
	yesterday = (datetime.today() - timedelta(2))
	users = User.objects.filter(date_joined__gt = yesterday);
	return str(users.count())
		

def getNumEmailUsers():
	numEmailUsers = int(getTotalUsers()) - int(getNumFbUsers())
	return str(numEmailUsers)

def getNumGirls():
	numGirls = int(getTotalUsers()) - int(getNumBoys())
	return str(numGirls)

def getNumBoys():
	numBoys = 0;
	yesterday = (datetime.today() - timedelta(2))
	users = User.objects.filter(date_joined__gt = yesterday);
	for user in users:
	  try:
		profile = Profile.objects.get(user=user)
		if (profile.gender == "male"):
			numBoys += 1;
	  except:
		continue;
	return str(numBoys)
	

def getAppleDevices():
	apple_counter = 0
	yesterday = (datetime.today() - timedelta(2))
	devices = Device2.objects.filter(date_registered__gt = yesterday)
	for device in devices:
		if device.manufacturer and device.manufacturer.name == "apple":
			apple_counter += 1
	return str(apple_counter)

def getTotalDevices():
	yesterday = (datetime.today() - timedelta(2))
	devices = Device2.objects.filter(date_registered__gt = yesterday);
	return str(devices.count())



print "total_steps="+ getTotalSteps()
print "total_users="+ getTotalUsers()
print "fb_users="+ getNumFbUsers()
print "email_users=" + getNumEmailUsers()
print "numboys="+ getNumBoys()
print "numgirls="+ getNumGirls()
new_total_dev = getTotalDevices()
print "new_total_devices="+ new_total_dev
new_apple_dev = getAppleDevices()
print "new_apple_devices="+ new_apple_dev
new_other_dev = str(int(new_total_dev) - int(new_apple_dev))
print "new_other_devices="+ new_other_dev




stat = createStat()
stat.active_users = getActiveUsers()
stat.total_users = getTotalUsers()
stat.total_steps = getTotalSteps()
stat.fb_users = getNumFbUsers()
stat.email_users = getNumEmailUsers()
stat.num_of_girls = getNumGirls()
stat.num_of_boys = getNumBoys()
stat.new_total_dev = new_total_dev
stat.new_apple_dev = new_apple_dev
stat.new_other_dev = new_other_dev
stat.save();

text_content = "active_users=" + stat.active_users + "\ntotal_users=" + stat.total_users + "\nnew_total_dev=" + stat.new_total_dev + "\nnew_apple_dev=" + stat.new_apple_dev + "\nnew_other_dev=" + stat.new_other_dev + "\ntotal_steps=" + stat.total_steps + "\nfb_users=" + stat.fb_users + "\nemail_users=" + stat.email_users
subject, from_email, to = 'Adimsayar Otomatik Rapor', 'adimsayarbilgi@gmail.com', "ozkolonur@gmail.com"
msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
msg.send()







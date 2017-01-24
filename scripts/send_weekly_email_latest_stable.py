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
from time import sleep
from content.models import *
from body_info.views import get_bmi_widget
from automatic_emails.views import *

thread_number = None;
if len(sys.argv) == 2:
	if int(sys.argv[1]) <= 3 and int(sys.argv[1]) >= 0:
		thread_number = int(sys.argv[1])
		print 'thread_number=' + str(thread_number)

def logit(msg):
	os.system("echo "+msg+" >> /tmp/maillog")

users = User.objects.all()
#users = User.objects.filter(email="ozkolonur@gmail.com")
counter = 0
no_email = 0
excounter = 0
itr = 0
for user in users:
	try:
		#this is for speed optimization, we should run 4 scripts in parallel
		if thread_number >= 0 and thread_number <= 3:
			if (user.id % 4 == thread_number):
				pass
			else:
				continue
		#is user active?
		if (user.is_active == True):
			pass
		else:
			no_email += 1
			msg = "id:"+str(user.id)+", email:"+user.email+",RESULT:USER_DISABLED"
			logit(msg)
			continue
		# does user wants this mails?
		profile = Profile.objects.get(user=user)
		if (profile.send_mail == True):
			pass
		else:
			no_email += 1
			msg = "id:"+str(user.id)+", email:"+user.email+",RESULT:NO_MAIL"
			logit(msg)
			continue
		#prepare e-mails
		html_content = prepare_weekly_email(user.email)
		text_content = strip_tags(html_content)
		subject, from_email, to = '[Haftalık rapor] Günlük hareketliliğinizi artıracak 20 ipucu', 'adimsayarbilgi@gmail.com', user.email
		msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
		counter += 1
		msg = "id:"+str(user.id)+", email:"+user.email+",RESULT:SENT"
		logit(msg)
	except Exception, err:
		#print err
		excounter += 1
		msg = str(err)
		logit(msg)
		continue
#send report mail for this thread
text_content = "mailcount=" + str(counter) + "\nno_mailcount=" + str(no_email) + "\nexcount=" + str(excounter)
to = ['ozkolonur@gmail.com', 'erdemozkol@gmail.com']
subject, from_email = 'Adimsayar send_weekly_email.py', 'adimsayarbilgi@gmail.com'
msg = EmailMultiAlternatives(subject, text_content, from_email, to)
msg.send()
sys.exit()

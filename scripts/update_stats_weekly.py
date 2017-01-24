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
from device2.models import Device2, Manufacturer
from mailing.models import UserReadMail

def getTotalUsers():
    now = datetime.now()
    lm = now - timedelta(days=now.weekday()+7)
    last_monday = datetime(lm.year, lm.month, lm.day)
    users = User.objects.filter(date_joined__gte = last_monday).order_by('date_joined');
    return str(users.count())

def getUserReadMails():
    now = datetime.now()
    lm = now - timedelta(days=now.weekday()+7)
    last_monday = datetime(lm.year, lm.month, lm.day)
    mails = UserReadMail.objects.filter(date_time__gte = last_monday);
    return str(mails.count())

total_weekly_users = getTotalUsers()
user_read_mails = getUserReadMails()
print "total_users="+ total_weekly_users
print "user_read_mails="+ user_read_mails

text_content = "total_weekly_users=" + total_weekly_users + "\nuser_read_mails=" + user_read_mails + "\n"
subject, from_email, to = 'Adimsayar Otomatik Rapor - Haftalik Rapor', 'adimsayarbilgi@gmail.com', "ozkolonur@gmail.com"
msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
msg.send()


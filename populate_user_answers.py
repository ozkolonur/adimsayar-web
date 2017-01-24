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
from mailing.models import Mailing
from mailing.views import prepare_mail_content
from poll.models import UserAnswer, Answer, Question
import threading

def get_answer(line):
    start = line.index('answer')
    end = line.index('&v=')
    tmp = line[start:end]
    tmp2 = tmp.split('&')
    for var in tmp2:
        variable = var.split('=')
        if variable[0] == 'answer':
            answer = variable[1]
        elif variable[0] == 'key_id':
            key_id = variable[1]
    return key_id, answer

counter = 0
results = dict()
for line in open('/home/ubuntu/adimsayar/logs/bugun3.log','r').readlines():
    if "answer" in line:
        user_id, answer_id = get_answer(line)
        print 'user_id='+user_id+" answer="+answer_id
        counter += 1
        results[user_id] = answer_id
print counter
print results
for user_id in results.keys():
    user = User.objects.get(id=long(user_id))
    answer = Answer.objects.get(id=long(results[user_id]))
    question = Question.objects.get(id=long(16))
    user_answer = UserAnswer(question=question, user=user, answer=answer)
    user_answer.save()
    answer.count += 1
    answer.save()






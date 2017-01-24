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
import threading


MAILING_LOCK_FILE = '/tmp/lockmail'
USE_MAILER_THREADS = True
MAX_NUM_OF_THREADS = 10
excounter = 0
no_mail = 0
counter = 0
threads = [None] * MAX_NUM_OF_THREADS 


def logit(msg):
    os.system("echo "+msg+" >> /tmp/maillog")



def lock_file_exists(lock_file):
    try:
        fp = open(lock_file, 'r')
        fp.close()
        return True
    except:
        return False

def create_lock_file(lock_file):
    fp = open(lock_file, 'w')
    fp.writelines('running')
    fp.close()

def remove_lock_file(lock_file):
    os.remove(lock_file)

def get_recipients_by_group(group_name):
#    if group_name == "all_plus_noemail_users":
    if group_name == "all":
        users = User.objects.all().exclude(is_active=False)
        return users
    #TODO:PROBLEM we need to find a cheap way of excluding send_mail = False
    elif group_name == "all_nontonotno":
        users = User.objects.all().exclude(is_active=False)
#        res = users.exclude(Profile.objects.filter(send_mail=False))
        for user in users:
            try:
                profile = Profile.objects.get(user=user)
                if profile.send_mail == False:
                    users.exclude(id=user.id)
            except Exception,err:
                continue
        return users

#    print ("I am thread "+ str(kwargs['tid']) + 
#        "I will send mail for " + kwargs['email'] + 
#        " using " + str(kwargs['mailing_id']) )
def mailer_thread(*args, **kwargs):
    email = kwargs['email']
    mailing_id = kwargs['mailing_id']
    try:
        #TODO:those users should be filtered in recipients_group...
        # does user wants this mails?
        recipient = User.objects.get(email=email)
        profile = Profile.objects.get(user=recipient)
        if (profile.send_mail == True):
            pass
        else:
            global no_email
            no_email += 1
            msg = "id:"+str(recipient.id)+", email:"+recipient.email+",RESULT:NO_MAIL"
            logit(msg)
        html_content = prepare_mail_content(recipient.email, mailing_id)
        text_content = strip_tags(html_content)
        subject, from_email, to = (mailing.subject,
            'adimsayarbilgi@gmail.com', recipient.email)
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        global counter
        counter += 1
        msg = "id:"+str(recipient.id)+", email:"+recipient.email+",RESULT:SENT"
        logit(msg)
    except Exception,err:
        print err
        global excounter
        excounter += 1
        msg = str(err)
        logit(msg)
    return None

#    print "executing with threads"
def execute_mailing_with_threads(recipients, mailing):
    recipient_itr = 0
    thread_itr = 0
    while(recipient_itr < len(recipients)):
        for thread_itr in range(0,MAX_NUM_OF_THREADS):
            thread = threads[thread_itr]
            if (threads[thread_itr] == None) or (not threads[thread_itr].is_alive()):
                if (recipient_itr < len(recipients)):
                    target_email = recipients[recipient_itr].email
                else:
                    break
                t = ( threading.Thread(target=mailer_thread, args=['none'], 
                    kwargs={
                         'tid': thread_itr, 
                         'email': target_email, 
                         'mailing_id': mailing.id }) )
                t.setDaemon(True)
                t.start()
                threads[thread_itr] = t
                recipient_itr += 1
            #if (recipient_itr + 1) < len(recipients):
            #    recipient_itr += 1
            #else:
            #    recipient_itr += len(recipients)
            #    break
    return None

def execute_mailing_without_threads(recipients, mailing):
    print "executing without threads"
    for recipient in recipients:
        try:
            #TODO:those users should be filtered in recipients_group...
            # does user wants this mails?
            profile = Profile.objects.get(user=recipient)
            if (profile.send_mail == True):
                pass
            else:
                global no_email
                no_email += 1
                msg = "id:"+str(recipient.id)+", email:"+recipient.email+",RESULT:NO_MAIL"
                logit(msg)
                continue
            html_content = prepare_mail_content(recipient.email, mailing.id)
            text_content = strip_tags(html_content)
            subject, from_email, to = (mailing.subject,
                'adimsayarbilgi@gmail.com', recipient.email)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            global counter
            counter += 1
            msg = "id:"+str(recipient.id)+", email:"+recipient.email+",RESULT:SENT"
            logit(msg)
        except Exception,err:
            print err
            global excounter
            excounter += 1
            msg = str(err)
            logit(msg)
            continue

def execute_mailing(mailing):
    if mailing.get_recipient_group_display() == "recipient_defined":
        recipients = User.objects.filter(email = mailing.recipient)
    else:
        recipients = get_recipients_by_group(mailing.get_recipient_group_display())

    print len(recipients)

    global counter
    counter = 0
    global no_email
    no_email = 0
    global excounter
    excounter = 0

    # this doesnt need to be MAX_NUM_OF_THREADS, no relation
    if len(recipients) > MAX_NUM_OF_THREADS:
        execute_mailing_with_threads(recipients, mailing)
    else:
        execute_mailing_without_threads(recipients, mailing)

    mailing.recipient_count = counter
    #mailing.completed = True
    mailing.save()

    text_content = ("mailcount=" + str(counter) + "\nno_mailcount=" + 
        str(no_email) + "\nexcount=" + str(excounter))
    to = ['ozkolonur@gmail.com', 'erdemozkol@gmail.com']
    subject, from_email = 'Adimsayar send_weekly_email.py', 'adimsayarbilgi@gmail.com'
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    print text_content
    msg.send()
    return None


if lock_file_exists(MAILING_LOCK_FILE):
    print "Already running"
    sys.exit()
else:
    create_lock_file(MAILING_LOCK_FILE)

print "Mailing Script Started"

try:
    two_hours_later = (datetime.today() + timedelta(seconds=60*60*2))
    mailings = (Mailing.objects.filter(target_date__lte = two_hours_later).
        exclude(is_active=False).exclude(completed=True))
    for mailing in mailings:
        execute_mailing(mailing)
except Exception,err:
    print err
    remove_lock_file(MAILING_LOCK_FILE)

sleep(3)
if lock_file_exists(MAILING_LOCK_FILE):
    remove_lock_file(MAILING_LOCK_FILE)
print "Mailing Script Stopped"
sys.exit()

#thread_number = None;
#if len(sys.argv) == 2:
#	if int(sys.argv[1]) <= 3 and int(sys.argv[1]) >= 0:
#		thread_number = int(sys.argv[1])
#		print 'thread_number=' + str(thread_number)
#


#run every 2 hour (or triggered by mailing.save())
#iterate mailings, pick one
#  is it active?
#  is completed?
#  time to send less than 2 hour
#  execute mailing

#
#find this week mailing_id
#get target users
#set recipient_count
#iterate for every user,given mailing id
#  count it
#  log_it
#send report mail

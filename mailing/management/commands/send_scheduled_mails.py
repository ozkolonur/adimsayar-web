from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from datetime import datetime
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
from mailing.models import *
from mailing.views import prepare_mail_content
from meas.models import Step, HourlyStepAvg
from body_info.models import BodyInfo
from django.db.models import Q
import threading
import os

MAILING_LOCK_FILE = '/tmp/lockmail'
USE_MAILER_THREADS = True
MAX_NUM_OF_THREADS = 64
excounter = 0
no_email = 0
counter = 0
threads = [None] * MAX_NUM_OF_THREADS 

def logit(msg):
    os.system("echo "+str(msg)+" >> /tmp/maillog")

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
    print "here"
    if group_name == "all-noweeklymail":
        users = User.objects.all().exclude(is_active=False)
        users_tmp = User.objects.all().exclude(is_active=False)
        for user in users_tmp:
            try:
                profile = Profile.objects.get(user=user)
                if not profile.send_mail_weekly:
                    users = users.exclude(id=user.id)
                    global no_email
                    no_email += 1
            except:
                users = users.exclude(id=user.id)
                global no_email
                no_email += 1
                continue
        return users
    elif group_name == "weight_update":
        users = User.objects.all().exclude(is_active=False)
        day_end = (datetime.today() - timedelta(36))
        #TODO: exclude profile.send_mail_weight_update == False
        day_start = (datetime.today() - timedelta(37))
        day_end_7days = (datetime.today() - timedelta(29))
        users = User.objects.filter(date_joined__gt = day_start, date_joined__lte = day_end)
        users_tmp = User.objects.filter(date_joined__gt = day_start, date_joined__lte = day_end)
        for user in users_tmp:
            body_infos = BodyInfo.objects.filter(user=user, date_time__gt = day_end_7days)
            if len(body_infos) > 0:
                users = users.exclude(id=user.id)
            try:
                profile = Profile.objects.get(user=user)
                if not profile.send_mail_weight_update:
                    users = users.exclude(id=user.id)
                    global no_email
                    no_email += 1
            except:
                users = users.exclude(id=user.id)
                global no_email
                no_email += 1
                continue
        return users
    elif group_name == "weight_update":
        body_infos = BodyInfo.objects.filter(user=user, date_time__gt = day_end_7days)
        if len(body_infos) > 0:
            users = users.exclude(id=user.id)
        return users

def mailer_thread(*args, **kwargs):
    email = kwargs['email']
    mailing_id = kwargs['mailing_id']
    try:
        recipient = User.objects.get(email=email)
        mailing_subject, html_content = prepare_mail_content(recipient.email, mailing_id)
        text_content = strip_tags(html_content)
        subject, from_email, to = (mailing_subject,
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
            mailing_subject, html_content = prepare_mail_content(recipient.email, mailing.id)
            text_content = strip_tags(html_content)
            subject, from_email, to = (mailing_subject,
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

    #if this is weekly_mail avoid multiple running script by cron
    #so make this mailing object completed before running
    if "weekly" in mailing.get_mail_type_display():
        mailing.completed = True
        mailing.save()

    # this doesnt need to be MAX_NUM_OF_THREADS, no relation
    if len(recipients) > MAX_NUM_OF_THREADS:
        execute_mailing_with_threads(recipients, mailing)
    else:
        execute_mailing_without_threads(recipients, mailing)

    mailing.recipient_count = counter
    mailing.completed = True
    mailing.save()

    # if this is weight update dont mark as completed
    if ("weight_update" == mailing.get_mail_type_display()):
        mailing.completed = False
        mailing.save()

    if ("won_badge" == mailing.get_mail_type_display()):
        mailing.delete()
        return None

    text_content = ("mailcount=" + str(counter) + "\nno_mailcount=" + 
        str(no_email) + "\nexcount=" + str(excounter))
    to = ['ozkolonur@gmail.com', 'erdemozkol@gmail.com']
    subject, from_email = 'Adimsayar MailRobot', 'adimsayarbilgi@gmail.com'
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    print text_content
    msg.send()
    return None


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'For every user calculates hourly step\
             stats and keep it in HourlyStepAvg table'

    def handle(self, *args, **options):
        if lock_file_exists(MAILING_LOCK_FILE):
            print "Already running"
            return
        else:
            create_lock_file(MAILING_LOCK_FILE)

        print "Mailing Script Started"
        try:
            now = datetime.today()

            #ugly hack for weight update mails
            if (now.hour == 10):
                mailing = Mailing.objects.filter(Q(mail_type=GET_MAIL_TYPE['weight_update']))[0]
                execute_mailing(mailing)

            two_hours_later = (now + timedelta(seconds=60*60*2))
            mailings = (Mailing.objects.
                filter(Q(target_date__lte = two_hours_later)|Q(when=GET_WHEN['immediately'])).
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
        return

        self.stdout.write('Successfully completed\n')






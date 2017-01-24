from django.core.management.base import BaseCommand, CommandError
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
import smtplib, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def send_mail_generic2(send_from, send_to, subject, text, files=[], server="localhost"):
    assert type(send_to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        Encoders.encode_base64(part)
        #part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        part.add_header('Content-Disposition', 'attachment; filename="adimsayar.txt"')
        msg.attach(part)

    smtp = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()



class Command(BaseCommand):
    args = '<to subject text ...>'
    help = 'sends an mail'
    def handle(self, *args, **options):
        print "Simple Send Mail"
        subject=args[1]
        #files = ['/tmp/adimsayar.apk']
        text = args[2]
        send_from = "adimsayarbilgi@gmail.com"
        send_to = args[0]
        print send_to
        print subject
        print text
        msg = EmailMultiAlternatives(subject, text, send_from, [send_to])
        msg.send()
        #send_mail_generic(subject=subject,send_to=to,text=text_content,files=attachment)
        #execute_mailing(subject=subject,to=to,text=text_content,files=attachment)
        self.stdout.write('Successfully completed\n')






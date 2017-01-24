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
import md5, hashlib, urllib
from random import randrange
import time
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from body_info.models import BodyInfo
from datetime import datetime, timedelta


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'For every user calculates hourly step\
             stats and keep it in HourlyStepAvg table'

    def handle(self, *args, **options):
        email = args[0]
        user = User.objects.get(email=email)
        user.delete()





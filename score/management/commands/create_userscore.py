from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from score.models import UserScore
from datetime import datetime, timedelta
from core.models import Profile
import random

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'For every user calculates hourly step\
             stats and keep it in HourlyStepAvg table'

    def handle(self, *args, **options):
        print "Initial-creating userscores"
        users = User.objects.all()
        print str(len(users)) + " users found"
        for user in users:
            p = UserScore(user=user)
            #p.score = random.randint(1,1000)
            p.save()
        self.stdout.write('completed\n')
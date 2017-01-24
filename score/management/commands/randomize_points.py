from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from score.models import Ranking
from datetime import datetime, timedelta
from core.models import Profile
import random

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'For every user calculates hourly step\
             stats and keep it in HourlyStepAvg table'

    def handle(self, *args, **options):
        print "Randomize points started"
        profiles = UserScore.objects.all().order_by('-score')
        print str(len(profiles)) + " profiles found"
        i = 0
        for p in profiles:
            p.score = random.randint(1,1000)
            p.save()
        self.stdout.write('Randomize points stopped\n')
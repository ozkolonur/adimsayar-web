from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from score.models import UserScore
from datetime import datetime, timedelta
from core.models import Profile

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'For every user calculates hourly step\
             stats and keep it in HourlyStepAvg table'

    def handle(self, *args, **options):
        print "Update Rankings Weekly started"
        profiles = UserScore.objects.all()
        print str(len(profiles)) + " profiles found"
        for p in profiles:
            p.xscore = p.score / 100
            p.score = 0
            p.save()
        self.stdout.write('Update Rankings stopped\n')
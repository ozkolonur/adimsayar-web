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
        print "Update Rankings started"
        profiles = UserScore.objects.all().order_by('-score')
        print str(len(profiles)) + " profiles found"
        i = 0
        for p in profiles:
            i += 1
            p.score_rank = i
            p.save()
        self.stdout.write('Update Rankings stopped\n')
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from body_info.models import BodyInfo
from datetime import datetime


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'For every user calculates hourly step\
             stats and keep it in HourlyStepAvg table'

    def handle(self, *args, **options):
        #users = User.objects.all()
        body_infos = BodyInfo.objects.all()
        for bi in body_infos:
            bi.weight_float = float(bi.weight)
            bi.save()
            print str(bi.id)
        self.stdout.write('Successfully completed\n')
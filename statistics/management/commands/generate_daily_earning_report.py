from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
import urllib
import json
from datetime import datetime,timedelta

def get_earnings():
    yesterday = datetime.today() - timedelta(days=1)
    startDate = yesterday.strftime('%Y-%m-%d')
    endDate = yesterday.strftime('%Y-%m-%d')
    metric = 'EARNINGS'
    access_token = 'ya29.AHES6ZS_OOHl34IrPvWn-xL2LOBGLL7TidF7znRUJZOYIc_c79k7jQ'
    url = ("https://www.googleapis.com/adsense/v1.1/reports/?" + 
        urllib.urlencode(dict(access_token=access_token,startDate=startDate,endDate=endDate,metric=metric)))
    print url
    me_json = urllib.urlopen(url)
    resp = json.load(me_json)
    print resp
    return 'TOTAL:'+ str(resp['totals'][0])

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'For every user calculates hourly step\
             stats and keep it in HourlyStepAvg table'

    def handle(self, *args, **options):
        earning = get_earnings()
        text_content = get_earnings() + '\nnever give-up\n'
        subject, from_email, to = 'Adimsayar Earnings', 'adimsayarbilgi@gmail.com', "ozkolonur@gmail.com"
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.send()

        self.stdout.write('Successfully completed\n')






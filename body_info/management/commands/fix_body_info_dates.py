from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from body_info.models import BodyInfo
from datetime import datetime, timedelta
from core.models import Profile


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'For every user calculates hourly step\
             stats and keep it in HourlyStepAvg table'

    def handle(self, *args, **options):
        #one time script
        #date of creation
        no_location = 0
        istanbul = 0
        izmir = 0
        ankara = 0
        somewhere = 0
        profiles = Profile.objects.all()
        for profile in profiles:
            if profile.user_location:
                print profile.user_location.city
                if profile.user_location.city.name == u'Istanbul':
                    istanbul += 1
                elif profile.user_location.city.name == u'Ankara':
                    ankara += 1
                elif profile.user_location.city.name == u'Izmir':
                    izmir += 1
                else:
                    somewhere += 1
            else:
                no_location += 1
        print "no_location="+str(no_location)
        print "istanbul="+str(istanbul)
        print "ankara="+str(ankara)
        print "izmir="+str(izmir)
        print "somewhere="+str(somewhere)
        #print len(body_infos)
        #for bi in body_infos:
        #    user_join_date = User.objects.get(id=bi.user.id).date_joined
        #    bi.date_time = user_join_date + timedelta(days=1)
        #    bi.save()
        #    print str(user_join_date)
        #    print str(bi.date_time)
        self.stdout.write('Successfully closed poll\n')
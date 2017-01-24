from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from core.models import Profile
from body_info.models import BodyInfo
from meas.models import Step
from score.models import Point
from venue.models import Venue, Checkin
from badges.models import BadgeToUser
from device2.models import Device2
from poll.models import UserAnswer
from mailing.models import UserReadMail
from datetime import datetime,timedelta
from statistics.models import DailyStats


'''
class DailyStats(models.Model):
    stat_time = models.DateTimeField(auto_now_add=True)
    date_time = models.DateTimeField()
    num_User = models.IntegerField(default=0)
    num_UserDisabled = models.IntegerField(default=0)
    num_UserNoEmail = models.IntegerField(default=0)
    num_UserRegFb = models.IntegerField(default=0)
    num_UserRegEmail = models.IntegerField(default=0)
    num_BodyInfo = models.IntegerField(default=0)
    num_Step = models.IntegerField(default=0)
    num_BadgeToUser = models.IntegerField(default=0)
    num_Point = models.IntegerField(default=0)
    num_Device2 = models.IntegerField(default=0)
    num_UserAnswer = models.IntegerField(default=0)
    num_UserReadMail = models.IntegerField(default=0)
    num_Venue = models.IntegerField(default=0)
    num_Checkin = models.IntegerField(default=0)
    def chg_User(self):
        return 100
        #TODO: return num_User_today - num_User_yesterday
'''

def num_User(date):
    users = User.objects.filter(date_joined__day=date.day, 
        date_joined__month=date.month, date_joined__year=date.year)
    return len(users)

def num_UserDisabled(date):
    #users = User.objects.filter(date_joined__day=date.day, 
    #    date_joined__month=date.month, date_joined__year=date.year, is_active=False)
    users = User.objects.filter(date_joined__lte=date, is_active=False)
    return len(users)

def num_UserNoEmail(date):
    users = User.objects.filter(date_joined__day=date.day, 
        date_joined__month=date.month, date_joined__year=date.year, is_active=True)

    counter = 0
    for user in users:
        try:
            prof = Profile.objects.get(user=user)
            if not prof.send_mail:
                counter += 1
        except Exception,err:
            print str(err) + " email="+user.email

    return counter

def num_UserLoginType(date):
    users = User.objects.filter(date_joined__day=date.day, 
        date_joined__month=date.month, date_joined__year=date.year, is_active=True)

    email = 0
    fb = 0
    for user in users:
        prof = Profile.objects.get(user=user)
        if prof.login_type == "fb":
            fb += 1
        elif prof.login_type == "email":
            email += 1

    return email, fb

def num_BodyInfo(date):
    objs = BodyInfo.objects.filter(date_time__day=date.day, 
        date_time__month=date.month, date_time__year=date.year)
    return len(objs)

def num_Step(date):
    objs = Step.objects.filter(date_time__day=date.day, 
        date_time__month=date.month, date_time__year=date.year)
    return len(objs)

def num_StepTotal(date):
    objs = Step.objects.filter(date_time__day=date.day, 
        date_time__month=date.month, date_time__year=date.year)

    counter = 0
    for step in objs:
        counter += int(step.total)

    return counter

def num_StepAvg(date):
    objs = Step.objects.filter(date_time__day=date.day, 
        date_time__month=date.month, date_time__year=date.year)

    counter = 0
    for step in objs:
        counter += int(step.total)

    result = 0
    if len(objs) > 0:
        result = counter / len(objs)

    return result

def num_BadgeToUser(date):
    objs = BadgeToUser.objects.filter(created__day=date.day, 
        created__month=date.month, created__year=date.year)
    return len(objs)

def num_Point(date):
    objs = Point.objects.filter(action_date__day=date.day, 
        action_date__month=date.month, action_date__year=date.year)
    return len(objs)

def num_Device2(date):
    objs = Device2.objects.filter(date_registered__day=date.day, 
        date_registered__month=date.month, date_registered__year=date.year)
    return len(objs)

def num_UserAnswer(date):
    objs = UserAnswer.objects.filter(date_time__day=date.day, 
        date_time__month=date.month, date_time__year=date.year)
    return len(objs)

def num_UserReadMail(date):
    objs = UserReadMail.objects.filter(date_time__day=date.day, 
        date_time__month=date.month, date_time__year=date.year)
    return len(objs)

def num_Venue(date):
    objs = Venue.objects.filter(date_time__day=date.day, 
        date_time__month=date.month, date_time__year=date.year)
    return len(objs)

def num_Checkin(date):
    objs = Checkin.objects.filter(date_time__day=date.day, 
        date_time__month=date.month, date_time__year=date.year)
    return len(objs)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def update_stats_date_range(start_date, end_date):
    for tday in daterange(start_date, end_date):
        print str(tday)
        stat, created = DailyStats.objects.get_or_create(date_time=tday)

        #print "numUser="+str(num_User(tday))
        stat.num_User = str(num_User(tday))

        #print "numUserDisabled="+str(num_UserDisabled(tday))
        stat.num_UserDisabled = str(num_UserDisabled(tday))

        #print "numUserEmail="+ str(num_UserNoEmail(tday))
        stat.num_UserNoEmail = str(num_UserNoEmail(tday))

        #TODO
        #num_email, num_fb =  num_UserLoginType(tday)
        num_email, num_fb =  0,0
        #print "numEmail="+str(num_email)
        #print "numEmail="+str(num_fb)

        #print "numBodyInfo="+str(num_BodyInfo(tday))
        stat.num_BodyInfo = str(num_BodyInfo(tday))

        #print "numUserAnswer="+str(num_UserAnswer(tday))
        stat.num_UserAnswer = str(num_UserAnswer(tday))

        #print "numUserReadMail="+str(num_UserReadMail(tday))
        stat.num_UserReadMail = str(num_UserReadMail(tday))

        #print "numDevice2="+str(num_Device2(tday))
        stat.num_Device2 = str(num_Device2(tday))

        #print "numStep="+str(num_Step(tday))
        stat.num_Step = str(num_Step(tday))

        #print "numStepTotal="+str(num_StepTotal(tday))
        stat.num_StepTotal = str(num_StepTotal(tday))

        #print "numStepAvg="+str(num_StepAvg(tday))
        stat.num_StepAvg = str(num_StepAvg(tday))

        #print "numPoint="+str(num_Point(tday))
        stat.num_Point = str(num_Point(tday))

        #print "numBadgeToUser="+str(num_BadgeToUser(tday))
        stat.num_BadgeToUser = str(num_BadgeToUser(tday))

        #print "numVenue="+str(num_Venue(tday))
        stat.num_Venue = str(num_Venue(tday))

        #print "numCheckin="+str(num_Checkin(tday))
        stat.num_Checkin = str(num_Checkin(tday))
        stat.save()


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'For every user calculates hourly step\
             stats and keep it in HourlyStepAvg table'

    def handle(self, *args, **options):
        if (len(args) > 0) and (args[0] == "regenerate"):
            print "Regenerating stats..."
            DailyStats.objects.all().delete()
            initial_date = datetime(2011, 11, 13)
            last_date = datetime.today() - timedelta(1)
            update_stats_date_range(initial_date, last_date)
        else:
            print "Updating daily stats..."
            initial_date = datetime.today() - timedelta(1)
            last_date = datetime.today()
            update_stats_date_range(initial_date, last_date)


        self.stdout.write('Successfully completed\n')






from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from meas.models import Step, HourlyStepAvg
from datetime import datetime


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'For every user calculates hourly step\
             stats and keep it in HourlyStepAvg table'

    def handle(self, *args, **options):
        users = User.objects.all()
        #users = User.objects.filter(email="gunay.satana@gmail.com")
        for user in users:
            print str(user.id)+":"+user.email
            last_7_steps = Step.objects.filter(user=user).order_by('-date_time')[:7]
            if len(last_7_steps) < 2:
                print "No step info"
                continue
            hourly_step_avg_int = [0]*24
            total_steps = 0
            total_calories = 0
            for step in last_7_steps:
                total_steps += step.total
                total_calories += step.calories
                hourly_step_list=step.steps.split(',')
                #print hourly_step_list
                for itr in range(0,24):
                     hourly_step_avg_int[itr] += int(hourly_step_list[itr])
            for itr in range(0,24):
                hourly_step_avg_int[itr] = hourly_step_avg_int[itr] / len(last_7_steps)
            #print hourly_step_avg_int
            hourly_step_avg_str = ['0']*24
            for itr in range(0,24):
                hourly_step_avg_str[itr] = str(hourly_step_avg_int[itr])

            tmp_device = None
            try:
                tmp_device = last_7_steps[0].device2
            except Exception,err:
                print str(err)
                continue

            record = HourlyStepAvg(user=user, 
                                   date_time=datetime.now(),
                                   steps=",".join(hourly_step_avg_str),
                                   total=total_steps/len(last_7_steps),
                                   calories=total_calories/len(last_7_steps),
                                   device = tmp_device)
            record.save()
            print str(len(last_7_steps)) + " email="+ user.email
        self.stdout.write('Successfully completed\n')
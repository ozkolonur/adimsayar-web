# -*- coding: utf-8 -*-
import badges
from meas.models import Step
from mailing.models import Mailing
from datetime import datetime, timedelta,time

class First10k(badges.MetaBadge):
    id = "First10k"
    model = Step
    one_time_only = True
    title = u'Bir günde 10 bin adım'
    description = u'İlk kez bir günde 10 bin adım yürüdünüz'
    level = "1"

    progress_start = 0
    progress_finish = 1

    def get_user(self, instance):
        return instance.user

    def get_progress(self, user):
        return 1

    def check_10k(self, instance):
        if (instance.total > 10000 and
            instance.total < 15000):
            return True
        else:
            return False

class First5k(badges.MetaBadge):
    id = "First5k"
    model = Step
    one_time_only = True
    title = u'Bir gunde 5 bin adım'
    description = u'İlk kez bir günde 5 bin adım yürüdünüz'
    level = "1"

    progress_start = 0
    progress_finish = 1

    def get_user(self, instance):
        return instance.user

    def get_progress(self, user):
        return 1

    def check_5k(self, instance):
        if (instance.total > 5000 and 
            instance.total < 10000):
            return True
        else:
            return False

class First15k(badges.MetaBadge):
    id = "First15k"
    model = Step
    one_time_only = True
    title = u'Bir gunde 15 bin adım'
    description = u'İlk kez bir günde 15 bin adim yürüdünüz'
    level = "1"

    progress_start = 0
    progress_finish = 1

    def get_user(self, instance):
        return instance.user

    def get_progress(self, user):
        return 1

    def check_15k(self, instance):
        if (instance.total > 15000):
            return True
        else:
            return False

class First70k(badges.MetaBadge):
    id = "First70k"
    model = Step
    one_time_only = True
    title = u'Bir haftada 70 bin adım'
    description = u'Bir haftada 10 bin adım yürüdünüz'
    level = "1"

    progress_start = 0
    progress_finish = 1

    def get_user(self, instance):
        return instance.user

    def get_progress(self, user):
        return 1

    #Not high performance but ok
    def check_weekly_70k(self, instance):
        total_steps = 0
        now = datetime.now()
        today = datetime.today()
        offset = ( (today.weekday()) % 7 ) + 1
        for day in range(0,offset):
            that_day = now - timedelta(days=day)
            step = Step.objects.filter(user=instance.user, 
                                       date_time__year=that_day.year, 
                                       date_time__month=that_day.month, 
                                       date_time__day=that_day.day)
            if step.count() > 0:
                total_steps += int(step[0].total)
        if (total_steps > 70000):
            return True
        else:
            return False

'''
from django.core.mail import EmailMultiAlternatives
from badges.signals import badge_awarded

def do_something_after_badge_is_awarded(sender, **kwargs):
    os.system("echo 0 >> /tmp/badge")
    mailing = Mailing(subject="rozet kazandiniz")
    mailing.save()
    return None

badge_awarded.connect(do_something_after_badge_is_awarded, sender=First5k)
badge_awarded.connect(do_something_after_badge_is_awarded, sender=First10k)
badge_awarded.connect(do_something_after_badge_is_awarded, sender=First15k)
'''


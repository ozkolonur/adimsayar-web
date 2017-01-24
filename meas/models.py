# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils.translation import ugettext as _
from device2.models import *
from score.models import Point

def steps2_to_steps(steps2):
    steps2_list_str = steps2[1:-1].split(',')
    steps_list_str = ['0'] * 24
    for i in range(0,23):
        hour_total = 0
        for j in range(1,13):
            hour_total += int(steps2_list_str[(12*i)+j])
        steps_list_str[i] = str(hour_total)
    steps_list = ",".join(steps_list_str)
    return steps_list

def steps_to_steps2(steps):
    steps2 = ['0']*288
    steps_list_str = steps.split(',')
    for i in range(0,24):
        steps2[i*12] = steps_list_str[i]
    steps2_str = ','.join(steps2)
    result = '['+steps2_str+']'
    return result

def steps_get_total(steps2):
    steps2_list_str = steps2[1:-1].split(',')
    total = 0
    for i in range(0,288):
        total += int(steps2_list_str[i])
    return total


class Step(models.Model):
    __total = 0

    user = models.ForeignKey(User)
    date_time = models.DateTimeField('date published')
    steps = models.CharField(max_length=1024)
    steps2 = models.CharField(max_length=2048, blank=True, null=True)
    am = models.CharField(max_length=512, blank=True, null=True)
    total = models.IntegerField(default=0)
    calories = models.FloatField(default=0)
    device2 = models.ForeignKey(Device2)

    def __init__(self, *args, **kwargs):
        super(Step, self).__init__(*args, **kwargs)
        self.__total = int(self.total)

    def save(self, *args, **kwargs):
        new_steps = self.total - int(self.__total)
        if  (new_steps > 0):
            user = User.objects.get(id=self.user_id)
            p = Point(user=user, action_name="W", action_param=new_steps, 
                 points_earned=(int(new_steps)/50))
            p.save()
        if (self.steps == "") and (self.steps2 != ""):
            self.steps = steps2_to_steps(self.steps2)
        elif (self.steps2 == "") and (self.steps != ""):
            self.steps2 = steps_to_steps2(self.steps)
        self.total = steps_get_total(self.steps2)
        super(Step,self).save(*args, **kwargs)
        self.__total = self.total

    def __unicode__(self):
        result = str(self.date_time)
        return result

class HourlyStepAvg(models.Model):
    user = models.ForeignKey(User)
    date_time = models.DateTimeField('date published')
    steps = models.CharField(max_length=1024)
    total = models.IntegerField(default=0)
    calories = models.FloatField(default=0)
    device = models.ForeignKey(Device2)
    def __unicode__(self):
        result = str(self.date_time)
        return result

class DietSuggestion(models.Model):
    suggestion =models.CharField(max_length=1024)
    def __unicode__(self):
        return self.suggestion

class CaloriesSuggestion(models.Model):
    suggestion =models.CharField(max_length=1024)
    def __unicode__(self):
        return self.suggestion

import meta_badges
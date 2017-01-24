# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

LIFESTYLE_CHOICES = ( ('1', _('Sedentary')), ('2', _('Low Activity')), ('3', _('Mid Activity')), ('4', _('High Activity')), ('5', _('Very High Activity')),)
GENDER_CHOICES = ( ('F', _('Female')), ('M', _('Male')),)

class BodyInfo(models.Model):
    user = models.ForeignKey(User)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, blank=True, null=True)
    date_time = models.DateTimeField('date_time', auto_now_add=True)
    age = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    weight_float = models.FloatField(blank=True, null=True)
    weight_goal = models.FloatField(blank=True, null=True)
    weight_goal_duration = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField()
    lifestyle = models.CharField(max_length=3, choices=LIFESTYLE_CHOICES, blank=True, null=True)
    bmr = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def ideal_weight(self):
        if (self.age <=24 ):
            bmi_advice = 22
        elif (25 <= self.age <=34):
            bmi_advice = 23
        elif (35 <= self.age <=44):
            bmi_advice = 23
        elif (45 <= self.age <=54):
            bmi_advice = 24
        elif (55 <= self.age <=65):
            bmi_advice = 25
        else:
            bmi_advice = 26

        if (self.height!=None and self.weight!=None):
            height,weight = float(self.height),float(self.weight)
            bmi = weight/((height/100)*(height/100))
            weight_advice = int(bmi_advice *((height/100)*(height/100)))
        return weight_advice

    def obesity_weight(self):
        height,weight = float(self.height),float(self.weight)
        obesity_weight = ((height/100)*(height/100)) * 30
        return int(obesity_weight)

    def bmi(self):
        res = (self.weight / ((self.height/100.00) * (self.height/100.00)))
        if res > 0 and res < 50:
            return "%.2f" % res
        else:
            return None

    def bmi_prime(self):
        res = ((self.weight / ((self.height/100.00) * (self.height/100.00))) / 25.00 )
        if res > 0 and res < 2:
            return "%.2f" % res
        else:
            return None

    def __unicode__(self):
        return u'%s' % self.user.username

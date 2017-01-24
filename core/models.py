# -*- coding: utf-8 -*-
from django.db import models
from userprofile.models import BaseProfile
from django.utils.translation import ugettext as _
from django.conf import settings
from ad.models import Tag
from meas.models import Step
from diet.models import Diet
from body_info.models import BodyInfo
from django.contrib.auth.models import User
import datetime
import os

def logit(msg):
    os.system("echo "+str(msg)+" >> /tmp/profilesavelogs")


class Country(models.Model):
	name = models.CharField(max_length=64, blank=True)
	shortcode = models.CharField(max_length=16, blank=True)
	cnt = models.PositiveIntegerField(default=0)
	def __unicode__(self):
		return self.name

class City(models.Model):
	country = models.ForeignKey(Country)
	name = models.CharField(max_length=64, blank=True)
	cnt = models.PositiveIntegerField(default=0)
	def __unicode__(self):
		return self.name
	def country_name(self):
		return self.country.name


class Isp(models.Model):
	name = models.CharField(max_length=128, blank=True)
	cnt = models.PositiveIntegerField(default=0)
	def __unicode__(self):
		return self.name

class Location(models.Model):
	country = models.ForeignKey(Country)
	city = models.ForeignKey(City)
	lon = models.CharField(max_length=32, blank=True)
	lan = models.CharField(max_length=32, blank=True)
	def __unicode__(self):
		return self.city.name

GENDER_CHOICES = ( ('F', _('Female')), ('M', _('Male')), ('male', _('Male')), ('female', _('Female')),)
LIFESTYLE_CHOICES = ( ('1', _('Sedentary')), ('2', _('Low Activity')), ('3', _('Mid Activity')), ('4', _('High Activity')), ('5', _('Very High Activity')),)


class Profile(BaseProfile):
    __height = None
    __weight = None
    __age = None
    __ip_addr = None
    __lifestyle = None

    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        self.__height = self.height
        self.__weight = self.weight
        self.__age = self.age
        self.__ip_addr = self.ip_addr
        self.__lifestyle = self.lifestyle

    def save(self, *args, **kwargs):
        logit("profsave1")
        if (self.height != self.__height or
            self.weight != self.__weight or
            self.lifestyle != self.__lifestyle or
            self.age != self.__age) and self.age and self.weight and self.height and self.gender:
            user = User.objects.get(id=self.user_id)
            logit("profsave2")
            body_info = BodyInfo(user=user, height=self.height, weight=self.weight, 
                age=self.age, lifestyle=self.lifestyle)
            logit("profsave3")
            try:
                body_info.save()
            except Exception,err:
                logit("binfosave:"+str(err))
                pass
        super(Profile,self).save(*args, **kwargs)
        logit("profsave4")
        self.__height = self.height
        self.__weight = self.weight
        self.__age = self.age
        self.__ip_addr = self.ip_addr

    firstname = models.CharField(max_length=255, blank=True)
    surname = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    height = models.IntegerField(null=True, blank=True, max_length=3)
    weight = models.IntegerField(null=True, blank=True, max_length=3)
    age = models.IntegerField(null=True, blank=True, max_length=3)
    lifestyle = models.CharField(max_length=3, choices=LIFESTYLE_CHOICES, blank=True, null=True)
    total_step = models.BigIntegerField(default=0,null=True, blank=True)
    send_mail = models.BooleanField(default=True)
    ip_addr = models.CharField(max_length=32, blank=True, null=True)
    user_location = models.ForeignKey(Location, null=True, blank=True)
    isp = models.ForeignKey(Isp, null=True, blank=True)
    overload_site = models.IntegerField(null=True, max_length=3, blank=True)
    diet = models.ForeignKey(Diet,blank=True, null=True)
    nickname_is_set = models.BooleanField(default=False)
    send_mail_weekly = models.BooleanField(default=True)
    send_mail_weight_update = models.BooleanField(default=True)
    send_mail_won_badge = models.BooleanField(default=True)
    send_mail_messages = models.BooleanField(default=True)
    send_mail_diet = models.BooleanField(default=True)
    send_mail_news = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)





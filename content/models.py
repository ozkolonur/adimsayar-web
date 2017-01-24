# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _

WHEN_CHOICES = (
				(0,_('time_defined')),
				(1,_('after_wake_up')),
				(2,_('breakfast')),
				(3,_('snack_10')),
				(4,_('lunch')),
				(5,_('snack_14')),
				(6,_('snack_15')),
				(7,_('snack_17')),
				(8,_('dinner')),
				(9,_('snack_21')),
				(10,_('before_sleep')),
				(11,_('monday')),
				(12,_('tuesday')),
				(13,_('wednesday')),
				(14,_('thursday')),
				(15,_('friday')),
				(16,_('saturday')),
				(17,_('sunday')),
				)

class ActionMsg(models.Model):
    odemeid = models.CharField(max_length=72)
    tutar = models.CharField(max_length=72)
    date_time = models.DateTimeField('date published', auto_now_add=True)
    def __unicode__(self):
        result = str(self.tutar)
        return result

class Content(models.Model):
    title = models.CharField(max_length=72)
    page = models.CharField(max_length=72)
    text = models.TextField(null=True, blank=True)
    date_time = models.DateTimeField('date published', auto_now_add=True)
    locale = models.CharField(max_length=8, blank=True, null=True)
    def __unicode__(self):
        result = str(self.title)
        return result

class News(models.Model):
	text = models.TextField(null=True, blank=True)		
	name = models.CharField(max_length=255, blank=True)
	date_time = models.DateTimeField('date published', auto_now_add=True)
	locale = models.CharField(max_length=8, blank=True)
	def __unicode__(self):
		return self.name

class Tweet(models.Model):
	message = models.CharField(max_length=140, null=True, blank=True)
	when = models.PositiveIntegerField(choices=WHEN_CHOICES, default=11)
	time = models.TimeField(null=True, blank=True)
	dom = models.PositiveIntegerField(null=True, blank=True)
	mon = models.PositiveIntegerField(null=True, blank=True)
	dow = models.PositiveIntegerField(null=True, blank=True)
	locale = models.CharField(max_length=8, blank=True)
	def __unicode__(self):
		return self.message



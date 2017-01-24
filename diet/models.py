# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.
ATOM_CHOICES = (
				(0,_('sound_1')),
				(1,_('sound_2')),
				(2,_('sound_3')),
				)

GROUP_CHOICES = (
				(0,_('group_1')),
				(1,_('group_2')),
				(2,_('group_3')),
				)

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
				)


class DietDefinition(models.Model):
	name = models.CharField(max_length=128)
	desc = models.TextField()
	group = models.PositiveIntegerField(choices=GROUP_CHOICES)
	rating = models.DecimalField(max_digits=5, decimal_places=1, default=0)
	diet_rate = models.PositiveIntegerField()
	rate_count = models.PositiveIntegerField()
	price = models.CharField(max_length=8)
	coupons = models.CharField(max_length=128)
	datetime = models.DateTimeField(auto_now_add = True)
	def __unicode__(self):
		return self.name	
			
	def save(self, **kwargs):
		if self.rate_count > 0:
			rating = Decimal(self.diet_rate)/Decimal(self.rate_count).quantize(Decimal('0.1'))
			self.rating = rating
		else:
			self.rating = 0
		super(DietDefinition, self).save(**kwargs)	

class Atom(models.Model):
	diet = models.ForeignKey(DietDefinition)
	when = models.PositiveIntegerField(choices=WHEN_CHOICES)
	time = models.TimeField(null=True, blank=True)
	dom = models.PositiveIntegerField(null=True, blank=True)
	mon = models.PositiveIntegerField(null=True, blank=True)
	dow = models.PositiveIntegerField(null=True, blank=True)
	message = models.TextField()
	url = models.URLField(null=True, blank=True)
	sound =models.PositiveIntegerField(choices=ATOM_CHOICES, null=True, blank=True)
	done = models.BooleanField(default=False)
	points = models.IntegerField(null=True, blank=True)
	def __unicode__(self):
		return  u'%s' % self.time

class Diet(models.Model):
	user = models.ForeignKey(User)
	diet_definition = models.ForeignKey(DietDefinition)
	start_date = models.DateTimeField(blank=True, null=True)
	finish_date = models.DateTimeField(blank=True, null=True)
	initial_weight = models.PositiveIntegerField(blank=True, null=True, max_length=3)
	current_weight = models.PositiveIntegerField(blank=True, null=True, max_length=3)
	target_weight = models.PositiveIntegerField(blank=True, null=True, max_length=3)
	datetime = models.DateTimeField(auto_now_add = True)
	def __unicode__(self):
		return self.diet_definition.name

# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

ACTION_NAME_CHOICES = ( ('W', _('Walking')), ('R', _('Running')),)

class VenueCategory(models.Model):
    name = models.CharField(max_length=128)
    icon = models.CharField(max_length=255, blank=True, null=True)
    def __unicode__(self):
        return u'%s' % self.name

class Venue(models.Model):
    venue_id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=255, blank=True, null=True)
    icon = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(VenueCategory, blank=True, null=True)
    mayor = models.ForeignKey(User, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    points = models.PositiveIntegerField(default=0, blank=True, null=True)
    checkins = models.PositiveIntegerField(blank=True, null=True)
    likes = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    page_rank = models.PositiveIntegerField(default=False, null=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % self.name

from django.core.serializers.python import Serializer

class VenueSerializer(Serializer):
    def end_object( self, obj ):
        self._current['point'] = obj.point()
        self._current['icon'] = obj.icon()
        self._current['description'] = "Bu bir description"
        self._current['name'] = obj.name
        self._current['id'] = obj._get_pk_val()
        self.objects.append( self._current )


class Checkin(models.Model):
    user = models.ForeignKey(User)
    venue = models.ForeignKey(Venue)
    points = models.PositiveIntegerField(blank=True)
    date_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return u'%s' % self.name



'''
class 4SQVenue(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=128)
    name = models.CharField(max_length=256)
    contact = models.ForeignKey(4SQContact)
    location = models.ForeignKey(4SQLocation)
    category = models.ForeignKey(4SQCategory)
    verified = models.BooleanField(default=False)
    checkinsCount = models.PositiveIntegerField()
    usersCount = models.PositiveIntegerField()
    tipCount = models.PositiveIntegerField()
    likesCount = models.PositiveIntegerField()
    specialsCount = models.PositiveIntegerField()
    hereNowCount = models.PositiveIntegerField()
    date_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return u'%s' % self.name

class 4SQCategory(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=128)
    pluralName = models.CharField(max_length=128)
    shortName = models.CharField(max_length=128)
    icon = models.CharField(max_length=128)
    category = models.ForeignKey(4SQCategory)
    points = models.DateTimeField(auto_now_add=True)
    total_checkins = models.PositiveIntegerField()
    date_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return u'%s' % self.name
'''
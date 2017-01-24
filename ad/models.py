# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.

AD_TYPE_CHOICES = (
    (0,_('banner_mail')),
    (1,_('banner_web')),
    (2,_('banner_mobile')),
)


class Tag(models.Model):
    name = models.CharField(max_length=32)
    cnt = models.PositiveIntegerField(default=0)
    def __unicode__(self):
        return str(self.name)


class Ad(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    btype = models.PositiveIntegerField(choices=AD_TYPE_CHOICES)
    tags = models.ManyToManyField(Tag)
    text = models.TextField(null=True, blank=True)
    locale = models.CharField(max_length=8, blank=True)
    date_time = models.DateTimeField('date published', auto_now_add=True)
    impression = models.PositiveIntegerField(default=0)
    click = models.PositiveIntegerField(default=0)
    def __unicode__(self):
        return self.name
    def ctr(self):
        return u'%.5f' % (100* (float(self.click) / (float(self.impression) + 1)))


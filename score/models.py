# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

ACTION_NAME_CHOICES = ( ('W', _('Walking')), ('R', _('Running')),)

class Point(models.Model):
    user = models.ForeignKey(User)
    action_date = models.DateTimeField(auto_now_add=True)
    action_name = models.CharField(max_length=8,choices=ACTION_NAME_CHOICES)
    action_param = models.CharField(max_length=255, null=True, blank=True)
    points_earned = models.IntegerField()

    def save(self, *args, **kwargs):
        us, created = UserScore.objects.get_or_create(user=self.user)
        us.score += self.points_earned
        us.save()
        super(Point,self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.action_name

class UserScore(models.Model):
    user = models.ForeignKey(User)
    score = models.IntegerField(default=0,null=True, blank=True)
    xscore = models.IntegerField(default=0,null=True, blank=True)
    high_score = models.IntegerField(default=0,null=True, blank=True)
    last_week_score = models.IntegerField(default=0,null=True, blank=True)
    score_rank = models.IntegerField(default=0,null=True, blank=True)
    xscore_rank = models.IntegerField(default=0,null=True, blank=True)
    last_week_score_rank = models.IntegerField(default=0,null=True, blank=True)

    def save(self, *args, **kwargs):
        if  (self.score > self.high_score):
            self.high_score = self.score
        super(UserScore,self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.user

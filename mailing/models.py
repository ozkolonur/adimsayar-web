# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

MAIL_TYPES = ( 
    (1, _('weekly')),
    (2, _('reset_password')),
    (3, _('weight_update')),
    (4, _('won_badge')),
)
GET_MAIL_TYPE = dict(((y, x) for x, y in MAIL_TYPES))


MAIL_GROUPS = ( 
    (1, _('recipient_defined')),
    (2, _('all-noweeklymail')),
    (3, _('all')),
    (4, _('weight_update')),
    (5, _('this_week_new_users')),
    (6, _('users_with_verified_hardware')),
)
GET_MAIL_GROUP = dict(((y, x) for x, y in MAIL_GROUPS))

WHEN_CHOICES = (
    (0,_('time_defined')),
    (1,_('immediately')),
)
GET_WHEN = dict(((y, x) for x, y in WHEN_CHOICES))


class Mailing(models.Model):
    mail_type = models.PositiveIntegerField(max_length=3,choices=MAIL_TYPES)
    when = models.PositiveIntegerField(choices=WHEN_CHOICES)
    target_date = models.DateTimeField('target_date', null=True, blank=True)
    dom = models.PositiveIntegerField(null=True, blank=True)
    mon = models.PositiveIntegerField(null=True, blank=True)
    dow = models.PositiveIntegerField(null=True, blank=True)
    recipient_group = models.PositiveIntegerField(choices=MAIL_GROUPS)
    recipient = models.CharField(max_length=256, blank=True, null=True)
    template = models.CharField(default='mailing/template1.html',
        max_length=512, blank=True, null=True)
    subject = models.CharField(max_length=512, blank=True, null=True)
    show_ads = models.BooleanField(default=False)
    read_count = models.PositiveIntegerField(blank=True, null=True)
    revisit_count = models.PositiveIntegerField(blank=True, null=True)
    spam_count = models.PositiveIntegerField(blank=True, null=True)
    unsubscribe_count = models.PositiveIntegerField(blank=True, null=True)
    user_delete_count = models.PositiveIntegerField(blank=True, null=True)
    recipient_count = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.target_date)

class Element(models.Model):
    mailing = models.ForeignKey(Mailing)
    order = models.PositiveIntegerField()
    content = models.CharField(max_length=255,blank=True,null=True)
    function = models.CharField(max_length=255,blank=True,null=True)
    params = models.CharField(max_length=1024,blank=True,null=True)
    def __unicode__(self):
        return u'%s' % self.content

class UserReadMail(models.Model):
    user = models.ForeignKey(User)
    mailing = models.ForeignKey(Mailing)
    date_time = models.DateTimeField('date_time', auto_now_add=True)
    def __unicode__(self):
        return u'%s' % self.user.email



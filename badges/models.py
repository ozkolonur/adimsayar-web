from datetime import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.conf import settings

from badges.signals import badge_awarded
from badges.managers import BadgeManager
from mailing.models import *

if hasattr(settings, 'BADGE_LEVEL_CHOICES'):
    LEVEL_CHOICES = settings.BADGE_LEVEL_CHOICES
else:
    LEVEL_CHOICES = (
        ("1", "Bronze"),
        ("2", "Silver"),
        ("3", "Gold"),
        ("4", "Diamond"),
    )

class Badge(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ManyToManyField(User, related_name="badges", through='BadgeToUser')
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES)
    
    icon = models.ImageField(upload_to='badge_images')
    
    objects = BadgeManager()
    
    @property
    def meta_badge(self):
        from utils import registered_badges
        return registered_badges[self.id]
    
    @property
    def title(self):
        return self.meta_badge.title
    
    @property
    def description(self):
        return self.meta_badge.description
    
    def __unicode__(self):
        return u"%s" % self.title
    
    def get_absolute_url(self):
        return reverse('badge_detail', kwargs={'slug': self.id})
    
    def award_to(self, user):
        has_badge = self in user.badges.all()
        if self.meta_badge.one_time_only and has_badge:
            return False
        
        BadgeToUser.objects.create(badge=self, user=user)
                
        badge_awarded.send(sender=self.meta_badge, user=user, badge=self)
        
        message_template = "You just got the %s Badge!"
        user.message_set.create(message = message_template % self.title)
        
        return BadgeToUser.objects.filter(badge=self, user=user).count()

    def number_awarded(self, user_or_qs=None):
        """
        Gives the number awarded total. Pass in an argument to
        get the number per user, or per queryset.
        """
        kwargs = {'badge':self}
        if user_or_qs is None:
            pass
        elif isinstance(user_or_qs, User):
            kwargs.update(dict(user=user_or_qs))
        else:
            kwargs.update(dict(user__in=user_or_qs))
        return BadgeToUser.objects.filter(**kwargs).count()


class BadgeToUser(models.Model):
    badge = models.ForeignKey(Badge)
    user = models.ForeignKey(User)
    
    created = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        #TODO prepare email content
        if self.badge.id == "First70k":
            mailing = Mailing(mail_type = GET_MAIL_TYPE["won_badge"],
                          when = GET_WHEN["immediately"],
                          recipient_group = GET_MAIL_GROUP["recipient_defined"],
                          recipient = self.user.email,
                          template = "mailing/template1.html",
                          subject="Tebrikler!",
                          is_active=True,
                          completed=False,
                          )
            #mailing.save()
            element1 = Element(mailing=mailing, order=0, content="mail_header", 
                               function="mail_header_params")
            #element1.save()
            param = "{'badge_id':'" + str(self.badge.id) + "'}"
            element2 = Element(mailing=mailing, order=1, content="mail_won_badge", 
                        function="mail_won_badge_params", params=param)
            #element2.save()
            element3 = Element(mailing=mailing, order=2, content="mail_footer", 
                        function="mail_footer_params")
            #element3.save()
        super(BadgeToUser,self).save(*args, **kwargs)















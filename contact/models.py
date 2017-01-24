from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=50)
    from_email = models.EmailField()
    system_email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.CharField(max_length=1000)
    auto_replied = models.BooleanField(default=False)
    answered = models.BooleanField(default=False)
    send_error = models.BooleanField(default=False)
    error_email = models.CharField(blank=True,null=True,max_length=255)
    def __unicode__(self):
        return  u'%s'  % self.name
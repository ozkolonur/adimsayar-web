from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Manufacturer(models.Model):
	name = models.CharField(max_length=64, blank=True)
	cnt = models.PositiveIntegerField(default=0)
	def __unicode__(self):
		return self.name

class Model(models.Model):
	name = models.CharField(max_length=64, blank=True)
	manufacturer = models.ForeignKey(Manufacturer, null=True, blank=True)
	cnt = models.PositiveIntegerField(default=0)
	def __unicode__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=64, blank=True)
	cnt = models.PositiveIntegerField(default=0)
	def __unicode__(self):
		return self.name

class Device2(models.Model):
    device_id = models.CharField(primary_key=True, max_length=255)
    date_registered = models.DateTimeField(auto_now_add=True)
    swversion = models.CharField(max_length=32, blank=True, null=True)
    appversion = models.CharField(max_length=8, blank=True, null=True)
    serial_number = models.CharField(max_length=64, blank=True, null=True)
    imei = models.CharField(max_length=32, blank=True, null=True)
    sensivity = models.PositiveIntegerField(default=0)
    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True)
    model = models.ForeignKey(Model, blank=True, null=True)
    product = models.ForeignKey(Product, blank=True, null=True)
    user = models.ForeignKey(User)
    def __unicode__(self):
	    return self.device_id
    def user_email(self):
	    return self.user.email





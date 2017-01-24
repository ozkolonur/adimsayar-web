from django.db import models

class Statistics(models.Model):
		stat_time = models.DateTimeField('date published')
		total_users = models.CharField(max_length=32, blank=True)
		total_active_users=models.CharField(max_length=128, blank=True)
		fb_users=models.CharField(max_length=32, blank=True)
		email_users=models.CharField(max_length=32, blank=True)
		total_steps=models.CharField(max_length=128, blank=True)
		total_get=models.CharField(max_length=128, blank=True)
		total_clories=models.CharField(max_length=128, blank=True)
		number_of_users=models.CharField(max_length=32, blank=True)
		number_of_girls=models.CharField(max_length=32, blank=True)
		number_of_boys=models.CharField(max_length=32, blank=True)
		average_age=models.CharField(max_length=8, blank=True)
		average_weight=models.CharField(max_length=8, blank=True)
		average_height=models.CharField(max_length=8, blank=True)
		average_daily_steps=models.CharField(max_length=8, blank=True)
		total_android_install=models.CharField(max_length=32, blank=True)
		def __unicode__(self):
			return self.total_steps

class DailyStatistics(models.Model):
		stat_time = models.DateTimeField('date published')
		active_users = models.CharField(max_length=32, blank=True)
		total_steps=models.CharField(max_length=128, blank=True)
		total_clories=models.CharField(max_length=128, blank=True)
		total_users=models.CharField(max_length=32, blank=True)
		fb_users=models.CharField(max_length=32, blank=True)
		email_users=models.CharField(max_length=32, blank=True)
		new_total_dev = models.CharField(max_length=32, blank=True)
		new_apple_dev = models.CharField(max_length=32, blank=True)
		new_other_dev = models.CharField(max_length=32, blank=True)
		num_of_girls = models.CharField(max_length=32, blank=True)
		num_of_boys = models.CharField(max_length=32, blank=True)
		ad_income_android=models.CharField(max_length=32, blank=True)
		ad_request=models.CharField(max_length=32, blank=True)
		ad_click=models.CharField(max_length=32, blank=True)
		install_android=models.CharField(max_length=32, blank=True)
		page_visit=models.CharField(max_length=32, blank=True)
		fb_visit=models.CharField(max_length=32, blank=True)
		total_client_requests=models.CharField(max_length=32, blank=True)
		android_client_requests=models.CharField(max_length=32, blank=True)
		iphone_client_requests=models.CharField(max_length=32, blank=True)
		reserved4=models.CharField(max_length=32, blank=True)
		def __unicode__(self):
			return self.total_steps

class HttpReq(models.Model):
		req = models.CharField(max_length=1024, blank=True)
		resp = models.CharField(max_length=5, blank=True)
		cause = models.CharField(max_length=32, blank=True)

class AgeVsUser(models.Model):
		stat_time = models.DateTimeField(auto_now_add=True)
		age = models.PositiveIntegerField(default=0)
		num_of_girls = models.PositiveIntegerField(default=0)
		num_of_boys = models.PositiveIntegerField(default=0)
		num_of_users = models.PositiveIntegerField(default=0)

class BmiVsUser(models.Model):
		stat_time = models.DateTimeField(auto_now_add=True)
		bmi = models.CharField(max_length=8,default=0)
		num_of_girls = models.PositiveIntegerField(default=0)
		num_of_boys = models.PositiveIntegerField(default=0)
		num_of_users = models.PositiveIntegerField(default=0)

#TODO
#class HourVsStep(models.Model):
#		stat_time = models.DateTimeField(auto_now_add=True)
#		bmi = models.CharField(max_length=8,default=0)
#		num_of_boys = models.PositiveIntegerField(default=0)
#		num_of_girls = models.PositiveIntegerField(default=0)
#		num_of_users = models.PositiveIntegerField(default=0)

#TODO
class AvgDailyStep(models.Model):
		stat_time = models.DateTimeField(auto_now_add=True)
		girls_average = models.PositiveIntegerField(default=0)
		boys_average = models.PositiveIntegerField(default=0)
		users_average = models.PositiveIntegerField(default=0)

#TODO: A script which runs everyday should count objects
# view with selectable obj type should be implemented
class DailyStats(models.Model):
    date_time = models.DateTimeField()
    num_User = models.IntegerField(default=0)
    num_UserDisabled = models.IntegerField(default=0)
    num_UserNoEmail = models.IntegerField(default=0)
    num_UserRegFb = models.IntegerField(default=0)
    num_UserRegEmail = models.IntegerField(default=0)
    num_BodyInfo = models.IntegerField(default=0)
    num_Step = models.IntegerField(default=0)
    num_StepTotal = models.IntegerField(default=0)
    num_StepAvg = models.IntegerField(default=0)
    num_BadgeToUser = models.IntegerField(default=0)
    num_Point = models.IntegerField(default=0)
    num_Device2 = models.IntegerField(default=0)
    num_UserAnswer = models.IntegerField(default=0)
    num_Venue = models.IntegerField(default=0)
    num_Checkin = models.IntegerField(default=0)
    num_SupportReq = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.date_time)

    def chg_User(self):
        return 100
        #TODO: return num_User_today - num_User_yesterday



#TODO
# how does daily steps increased by membership
# get a user, list all steps by date
# cumulate




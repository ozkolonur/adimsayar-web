from statistics.models import *
from django.contrib import admin

class DailyStatisticsAdmin(admin.ModelAdmin):
	list_filter = ('stat_time',)
	list_display = ('stat_time','active_users','total_users','ad_income_android','install_android','page_visit','fb_users','email_users','num_of_girls','num_of_boys', 'total_client_requests')

class HttpReqAdmin(admin.ModelAdmin):
	list_display = ('req','resp', 'cause')

class AgeVsUserAdmin(admin.ModelAdmin):
	list_display = ('stat_time', 'age', 'num_of_users', 'num_of_girls', 'num_of_boys')

class BmiVsUserAdmin(admin.ModelAdmin):
	list_display = ('stat_time', 'bmi', 'num_of_users', 'num_of_girls', 'num_of_boys')

class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'num_User',)

admin.site.register(Statistics)
admin.site.register(DailyStatistics, DailyStatisticsAdmin)
admin.site.register(HttpReq, HttpReqAdmin)
admin.site.register(AgeVsUser, AgeVsUserAdmin)
admin.site.register(BmiVsUser, BmiVsUserAdmin)
admin.site.register(DailyStats, DailyStatsAdmin)



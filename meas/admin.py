from meas.models import *
from django.contrib import admin

class StepAdmin(admin.ModelAdmin):
    raw_id_fields = ('user','device2')
    list_filter = ('date_time',)
    list_display = ('date_time','steps','total','calories')

class HourlyStepAvgAdmin(admin.ModelAdmin):
    list_filter = ('date_time',)
    list_display = ('user','date_time','steps','total','calories')

admin.site.register(Step, StepAdmin)
admin.site.register(HourlyStepAvg, HourlyStepAvgAdmin)
admin.site.register(DietSuggestion)
admin.site.register(CaloriesSuggestion)

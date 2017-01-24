from django.contrib import admin
from models import BodyInfo

class BodyInfoAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('date_time', 'gender',  'height','weight','weight_float','age')

admin.site.register(BodyInfo, BodyInfoAdmin)


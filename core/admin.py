from core.models import Profile
from django.contrib import admin
from core.models import Location, Country, City, Isp

class ProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('user', 'height','weight','age','total_step')
    search_fields = ('surname', 'firstname','user__email')

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'shortcode', 'cnt')

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_name', 'cnt')
    list_filter = ['country']

class IspAdmin(admin.ModelAdmin):
    list_display = ('name', 'cnt')

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Location)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Isp, IspAdmin)


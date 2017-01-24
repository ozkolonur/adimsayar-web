from django.contrib import admin
from models import Venue

class VenueAdmin(admin.ModelAdmin):
    list_display = ('venue_id', 'name', 'lon',  'lat')

admin.site.register(Venue, VenueAdmin)

